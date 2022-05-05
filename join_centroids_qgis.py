"""
Model exported as python.
Name : centroids
Group : 
With QGIS : 32204
"""

from qgis.core import QgsProcessing
from qgis.core import QgsProcessingAlgorithm
from qgis.core import QgsProcessingMultiStepFeedback
from qgis.core import QgsProcessingParameterField
from qgis.core import QgsProcessingParameterVectorLayer
from qgis.core import QgsProcessingParameterFeatureSink
import processing


class Centroids(QgsProcessingAlgorithm):

    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterVectorLayer('parcels', 'Parcels', types=[QgsProcessing.TypeVectorPolygon], defaultValue=None))
        self.addParameter(QgsProcessingParameterField('parceladdress', 'Parcel Address', type=QgsProcessingParameterField.Any, parentLayerParameterName='parcels', allowMultiple=False, defaultValue=None))
        self.addParameter(QgsProcessingParameterField('owneraddress', 'Owner Address', type=QgsProcessingParameterField.Any, parentLayerParameterName='parcels', allowMultiple=False, defaultValue=None))
        self.addParameter(QgsProcessingParameterVectorLayer('polygons', 'Neighborhoods', types=[QgsProcessing.TypeVectorPolygon], defaultValue=None))
        self.addParameter(QgsProcessingParameterField('identifier', 'Neighborhood Identifier', type=QgsProcessingParameterField.Any, parentLayerParameterName='polygons', allowMultiple=False, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Joined_centroids', 'joined_centroids', optional=True, type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, defaultValue=None))

    def processAlgorithm(self, parameters, context, model_feedback):
        # Use a multi-step feedback, so that individual child algorithm progress reports are adjusted for the
        # overall progress through the model
        feedback = QgsProcessingMultiStepFeedback(5, model_feedback)
        results = {}
        outputs = {}

        # Fix geometries
        alg_params = {
            'INPUT': parameters['parcels'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['FixGeometries'] = processing.run('native:fixgeometries', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(1)
        if feedback.isCanceled():
            return {}

        # Generate Centroids
        alg_params = {
            'ALL_PARTS': False,
            'INPUT': outputs['FixGeometries']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['GenerateCentroids'] = processing.run('native:centroids', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(2)
        if feedback.isCanceled():
            return {}

        # Add latitude field
        alg_params = {
            'FIELD_LENGTH': 10,
            'FIELD_NAME': 'lat',
            'FIELD_PRECISION': 8,
            'FIELD_TYPE': 0,  # Float
            'FORMULA': "y(transform($geometry, layer_property(@layer, 'crs'),'EPSG:4326'))",
            'INPUT': outputs['GenerateCentroids']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['AddLatitudeField'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(3)
        if feedback.isCanceled():
            return {}

        # Add longitude field
        alg_params = {
            'FIELD_LENGTH': 10,
            'FIELD_NAME': 'lng',
            'FIELD_PRECISION': 8,
            'FIELD_TYPE': 0,  # Float
            'FORMULA': "x(transform($geometry, layer_property(@layer, 'crs'),'EPSG:4326'))",
            'INPUT': outputs['AddLatitudeField']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['AddLongitudeField'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(4)
        if feedback.isCanceled():
            return {}

        # Join attributes by location
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'INPUT': outputs['AddLongitudeField']['OUTPUT'],
            'JOIN': parameters['polygons'],
            'JOIN_FIELDS': parameters['identifier'],
            'METHOD': 0,  # Create separate feature for each matching feature (one-to-many)
            'PREDICATE': [5],  # within
            'PREFIX': '',
            'OUTPUT': parameters['Joined_centroids']
        }
        outputs['JoinAttributesByLocation'] = processing.run('native:joinattributesbylocation', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Joined_centroids'] = outputs['JoinAttributesByLocation']['OUTPUT']
        return results

    def name(self):
        return 'centroids'

    def displayName(self):
        return 'centroids'

    def group(self):
        return ''

    def groupId(self):
        return ''

    def createInstance(self):
        return Centroids()

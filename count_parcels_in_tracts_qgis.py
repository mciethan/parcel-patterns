"""
Model exported as python.
Name : tract_joins
Group : 
With QGIS : 32204
"""

from qgis.core import QgsProcessing
from qgis.core import QgsProcessingAlgorithm
from qgis.core import QgsProcessingMultiStepFeedback
from qgis.core import QgsProcessingParameterVectorLayer
from qgis.core import QgsProcessingParameterField
from qgis.core import QgsProcessingParameterFeatureSink
import processing


class Tract_joins(QgsProcessingAlgorithm):

    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterVectorLayer('parcelcentroids', 'Parcel Centroids', types=[QgsProcessing.TypeVectorPoint], defaultValue=None))
        self.addParameter(QgsProcessingParameterField('parcelid', 'Parcel ID', type=QgsProcessingParameterField.Any, parentLayerParameterName='parcelcentroids', allowMultiple=False, defaultValue=None))
        self.addParameter(QgsProcessingParameterVectorLayer('tracts', 'tracts', defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Wide_2016', 'wide_2016', optional=True, type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Joined_tracts_2016', 'joined_tracts_2016', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, defaultValue=None))

    def processAlgorithm(self, parameters, context, model_feedback):
        # Use a multi-step feedback, so that individual child algorithm progress reports are adjusted for the
        # overall progress through the model
        feedback = QgsProcessingMultiStepFeedback(9, model_feedback)
        results = {}
        outputs = {}

        # Join attributes by field value
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'FIELD': parameters['parcelid'],
            'FIELDS_TO_COPY': [''],
            'FIELD_2': parameters['parcelid'],
            'INPUT': 'Joined_layer_525d2b52_870d_4cd6_b4d4_f4a9f29e3542',
            'INPUT_2': 'C:/QGIS/Providence/parcel_chars_2016.csv',
            'METHOD': 1,  # Take attributes of the first matching feature only (one-to-one)
            'PREFIX': '',
            'OUTPUT': parameters['Wide_2016']
        }
        outputs['JoinAttributesByFieldValue'] = processing.run('native:joinattributestable', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Wide_2016'] = outputs['JoinAttributesByFieldValue']['OUTPUT']

        feedback.setCurrentStep(1)
        if feedback.isCanceled():
            return {}

        # Refactor fields
        alg_params = {
            'FIELDS_MAPPING': [{'expression': '"ASSESSPAR_"','length': 4,'name': 'ASSESSPAR_','precision': 0,'type': 10},{'expression': '"ASSESSPAR1"','length': 10,'name': 'ASSESSPAR1','precision': 0,'type': 10},{'expression': '"ASSESSPA_1"','length': 10,'name': 'ASSESSPA_1','precision': 0,'type': 10},{'expression': '"ASSESSPA_2"','length': 18,'name': 'ASSESSPA_2','precision': 0,'type': 10},{'expression': '"ASSESSPA_3"','length': 12,'name': 'ASSESSPA_3','precision': 0,'type': 10},{'expression': '"ASSESSPA_4"','length': 18,'name': 'ASSESSPA_4','precision': 0,'type': 10},{'expression': '"ASSESSPA_5"','length': 12,'name': 'ASSESSPA_5','precision': 0,'type': 10},{'expression': '"ASSESSPA_6"','length': 18,'name': 'ASSESSPA_6','precision': 0,'type': 10},{'expression': '"ASSESSPA_7"','length': 15,'name': 'ASSESSPA_7','precision': 0,'type': 10},{'expression': '"ASSESSPA_8"','length': 1,'name': 'ASSESSPA_8','precision': 0,'type': 10},{'expression': '"ASSESSPA_9"','length': 8,'name': 'ASSESSPA_9','precision': 0,'type': 10},{'expression': '"ASSESSP_10"','length': 12,'name': 'ASSESSP_10','precision': 0,'type': 10},{'expression': '"ASSESSP_11"','length': 6,'name': 'ASSESSP_11','precision': 0,'type': 10},{'expression': '"ASSESSP_12"','length': 10,'name': 'ASSESSP_12','precision': 0,'type': 4},{'expression': '"ASSESSP_13"','length': 5,'name': 'ASSESSP_13','precision': 0,'type': 2},{'expression': '"ASSESSP_14"','length': 5,'name': 'ASSESSP_14','precision': 0,'type': 2},{'expression': '"ASSESSP_15"','length': 20,'name': 'ASSESSP_15','precision': 0,'type': 10},{'expression': '"ASSESSP_16"','length': 10,'name': 'ASSESSP_16','precision': 0,'type': 14},{'expression': '"ASSESSP_17"','length': 10,'name': 'ASSESSP_17','precision': 0,'type': 14},{'expression': '"ASSESSP_18"','length': 20,'name': 'ASSESSP_18','precision': 0,'type': 10},{'expression': '"ASSESSP_19"','length': 5,'name': 'ASSESSP_19','precision': 0,'type': 2},{'expression': '"ASSESSP_20"','length': 250,'name': 'ASSESSP_20','precision': 0,'type': 10},{'expression': '"ASSESSP_21"','length': 50,'name': 'ASSESSP_21','precision': 0,'type': 10},{'expression': '"ASSESSP_22"','length': 18,'name': 'ASSESSP_22','precision': 11,'type': 6},{'expression': '"ASSESSP_23"','length': 18,'name': 'ASSESSP_23','precision': 11,'type': 6},{'expression': '"ASSESSP_24"','length': 10,'name': 'ASSESSP_24','precision': 0,'type': 4},{'expression': '"CAMA_OBJEC"','length': 10,'name': 'CAMA_OBJEC','precision': 0,'type': 4},{'expression': '"CAMA_PIN"','length': 54,'name': 'CAMA_PIN','precision': 0,'type': 10},{'expression': '"CAMA_AV_PI"','length': 50,'name': 'CAMA_AV_PI','precision': 0,'type': 10},{'expression': '"CAMA_CLASS"','length': 15,'name': 'CAMA_CLASS','precision': 0,'type': 10},{'expression': '"CAMA_PROPI"','length': 13,'name': 'CAMA_PROPI','precision': 0,'type': 10},{'expression': '"CAMA_PlatN"','length': 50,'name': 'CAMA_PlatN','precision': 0,'type': 10},{'expression': '"CAMA_Block"','length': 1,'name': 'CAMA_Block','precision': 0,'type': 10},{'expression': '"CAMA_LotNu"','length': 50,'name': 'CAMA_LotNu','precision': 0,'type': 10},{'expression': '"CAMA_SubLo"','length': 1,'name': 'CAMA_SubLo','precision': 0,'type': 10},{'expression': '"CAMA_UnitN"','length': 50,'name': 'CAMA_UnitN','precision': 0,'type': 10},{'expression': '"CAMA_MuniN"','length': 14,'name': 'CAMA_MuniN','precision': 0,'type': 10},{'expression': '"CAMA_FORMA"','length': 50,'name': 'CAMA_FORMA','precision': 0,'type': 10},{'expression': '"CAMA_ZIP_P"','length': 10,'name': 'CAMA_ZIP_P','precision': 0,'type': 10},{'expression': '"CAMA_Owner"','length': 80,'name': 'CAMA_Owner','precision': 0,'type': 10},{'expression': '"CAMA_Own_1"','length': 76,'name': 'CAMA_Own_1','precision': 0,'type': 10},{'expression': '"CAMA_Own_2"','length': 58,'name': 'CAMA_Own_2','precision': 0,'type': 10},{'expression': '"CAMA_Own_3"','length': 40,'name': 'CAMA_Own_3','precision': 0,'type': 10},{'expression': '"CAMA_Own_4"','length': 15,'name': 'CAMA_Own_4','precision': 0,'type': 10},{'expression': '"CAMA_Own_5"','length': 10,'name': 'CAMA_Own_5','precision': 0,'type': 10},{'expression': '"CAMA_Own_6"','length': 30,'name': 'CAMA_Own_6','precision': 0,'type': 10},{'expression': '"CAMA_LastB"','length': 12,'name': 'CAMA_LastB','precision': 0,'type': 10},{'expression': '"CAMA_LastP"','length': 10,'name': 'CAMA_LastP','precision': 0,'type': 10},{'expression': '"CAMA_LastD"','length': 20,'name': 'CAMA_LastD','precision': 0,'type': 10},{'expression': '"CAMA_LastS"','length': 18,'name': 'CAMA_LastS','precision': 11,'type': 6},{'expression': '"CAMA_Las_1"','length': 10,'name': 'CAMA_Las_1','precision': 0,'type': 14},{'expression': '"CAMA_Asses"','length': 18,'name': 'CAMA_Asses','precision': 11,'type': 6},{'expression': '"CAMA_Ass_1"','length': 18,'name': 'CAMA_Ass_1','precision': 11,'type': 6},{'expression': '"CAMA_Ass_2"','length': 18,'name': 'CAMA_Ass_2','precision': 11,'type': 6},{'expression': '"CAMA_TaxRo"','length': 1,'name': 'CAMA_TaxRo','precision': 0,'type': 10},{'expression': '"CAMA_State"','length': 1,'name': 'CAMA_State','precision': 0,'type': 10},{'expression': '"CAMA_MuniU"','length': 50,'name': 'CAMA_MuniU','precision': 0,'type': 10},{'expression': '"CAMA_Mun_1"','length': 50,'name': 'CAMA_Mun_1','precision': 0,'type': 10},{'expression': '"CAMA_AreaA"','length': 18,'name': 'CAMA_AreaA','precision': 11,'type': 6},{'expression': '"CAMA_AreaS"','length': 18,'name': 'CAMA_AreaS','precision': 11,'type': 6},{'expression': '"CAMA_NumBl"','length': 18,'name': 'CAMA_NumBl','precision': 11,'type': 6},{'expression': '"CAMA_NumUn"','length': 10,'name': 'CAMA_NumUn','precision': 0,'type': 4},{'expression': '"CAMA_YearB"','length': 10,'name': 'CAMA_YearB','precision': 0,'type': 4},{'expression': '"CAMA_NumFl"','length': 18,'name': 'CAMA_NumFl','precision': 11,'type': 6},{'expression': '"CAMA_GrBld"','length': 10,'name': 'CAMA_GrBld','precision': 0,'type': 4},{'expression': '"CAMA_Livin"','length': 10,'name': 'CAMA_Livin','precision': 0,'type': 4},{'expression': '"CAMA_NumBe"','length': 10,'name': 'CAMA_NumBe','precision': 0,'type': 4},{'expression': '"CAMA_NumBa"','length': 10,'name': 'CAMA_NumBa','precision': 0,'type': 4},{'expression': '"CAMA_NumHa"','length': 18,'name': 'CAMA_NumHa','precision': 11,'type': 6},{'expression': '"Shape_STAr"','length': 18,'name': 'Shape_STAr','precision': 11,'type': 6},{'expression': '"Shape_STLe"','length': 18,'name': 'Shape_STLe','precision': 11,'type': 6},{'expression': '"Shape_Leng"','length': 18,'name': 'Shape_Leng','precision': 11,'type': 6},{'expression': '"Shape_Area"','length': 18,'name': 'Shape_Area','precision': 11,'type': 6},{'expression': '"ownr_occd"','length': 12,'name': 'ownr_occd','precision': 11,'type': 6},{'expression': '"lat"','length': 10,'name': 'lat','precision': 8,'type': 6},{'expression': '"lng"','length': 10,'name': 'lng','precision': 8,'type': 6},{'expression': '"NAMELSAD"','length': 20,'name': 'NAMELSAD','precision': 0,'type': 10},{'expression': '"field_1"','length': 0,'name': 'field_1','precision': 0,'type': 10},{'expression': '"CAMA_PROPI_2"','length': 0,'name': 'CAMA_PROPI_2','precision': 0,'type': 10},{'expression': '"CAMA_UnitN_2"','length': 0,'name': 'CAMA_UnitN_2','precision': 0,'type': 10},{'expression': '"CAMA_MuniN_2"','length': 0,'name': 'CAMA_MuniN_2','precision': 0,'type': 10},{'expression': '"CAMA_FORMA_2"','length': 0,'name': 'CAMA_FORMA_2','precision': 0,'type': 10},{'expression': '"CAMA_ZIP_P_2"','length': 0,'name': 'CAMA_ZIP_P_2','precision': 0,'type': 10},{'expression': '"CAMA_Owner_2"','length': 0,'name': 'CAMA_Owner_2','precision': 0,'type': 10},{'expression': '"CAMA_Own_1_2"','length': 0,'name': 'CAMA_Own_1_2','precision': 0,'type': 10},{'expression': '"CAMA_Own_2_2"','length': 0,'name': 'CAMA_Own_2_2','precision': 0,'type': 10},{'expression': '"CAMA_Own_3_2"','length': 0,'name': 'CAMA_Own_3_2','precision': 0,'type': 10},{'expression': '"CAMA_Own_4_2"','length': 0,'name': 'CAMA_Own_4_2','precision': 0,'type': 10},{'expression': '"CAMA_Own_5_2"','length': 0,'name': 'CAMA_Own_5_2','precision': 0,'type': 10},{'expression': '"CAMA_Own_6_2"','length': 0,'name': 'CAMA_Own_6_2','precision': 0,'type': 10},{'expression': '"lat_2"','length': 0,'name': 'lat_2','precision': 0,'type': 10},{'expression': '"lng_2"','length': 0,'name': 'lng_2','precision': 0,'type': 10},{'expression': '"NAMELSAD_2"','length': 0,'name': 'NAMELSAD_2','precision': 0,'type': 10},{'expression': '"ALT_OWN_ADD"','length': 0,'name': 'ALT_OWN_ADD','precision': 0,'type': 10},{'expression': '"ALT_OWN_ADD_2"','length': 0,'name': 'ALT_OWN_ADD_2','precision': 0,'type': 10},{'expression': '"OWNER_INFO"','length': 0,'name': 'OWNER_INFO','precision': 0,'type': 10},{'expression': '"OWNER_AREA"','length': 0,'name': 'OWNER_AREA','precision': 0,'type': 10},{'expression': '"oo"','length': 0,'name': 'oo','precision': 0,'type': 4},{'expression': '"ia"','length': 0,'name': 'ia','precision': 0,'type': 4},{'expression': '"oa"','length': 0,'name': 'oa','precision': 0,'type': 4},{'expression': '"po"','length': 0,'name': 'po','precision': 0,'type': 4},{'expression': '"xi"','length': 0,'name': 'xi','precision': 0,'type': 4},{'expression': '"xf"','length': 0,'name': 'xf','precision': 0,'type': 4}],
            'INPUT': outputs['JoinAttributesByFieldValue']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['RefactorFields'] = processing.run('native:refactorfields', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(2)
        if feedback.isCanceled():
            return {}

        # Join parcels
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'INPUT': parameters['tracts'],
            'JOIN': outputs['RefactorFields']['OUTPUT'],
            'JOIN_FIELDS': ['oo'],
            'PREDICATE': [1],  # contains
            'SUMMARIES': [0],  # count
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['JoinParcels'] = processing.run('qgis:joinbylocationsummary', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(3)
        if feedback.isCanceled():
            return {}

        # Join owner_occd_sum
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'INPUT': outputs['JoinParcels']['OUTPUT'],
            'JOIN': outputs['RefactorFields']['OUTPUT'],
            'JOIN_FIELDS': ['oo'],
            'PREDICATE': [1],  # contains
            'SUMMARIES': [5],  # sum
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['JoinOwner_occd_sum'] = processing.run('qgis:joinbylocationsummary', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(4)
        if feedback.isCanceled():
            return {}

        # Join in_area_sum
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'INPUT': outputs['JoinOwner_occd_sum']['OUTPUT'],
            'JOIN': outputs['RefactorFields']['OUTPUT'],
            'JOIN_FIELDS': ['ia'],
            'PREDICATE': [1],  # contains
            'SUMMARIES': [5],  # sum
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['JoinIn_area_sum'] = processing.run('qgis:joinbylocationsummary', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(5)
        if feedback.isCanceled():
            return {}

        # Join out_area_sum
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'INPUT': outputs['JoinIn_area_sum']['OUTPUT'],
            'JOIN': outputs['RefactorFields']['OUTPUT'],
            'JOIN_FIELDS': ['oa'],
            'PREDICATE': [1],  # contains
            'SUMMARIES': [5],  # sum
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['JoinOut_area_sum'] = processing.run('qgis:joinbylocationsummary', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(6)
        if feedback.isCanceled():
            return {}

        # Join po_box_sum
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'INPUT': outputs['JoinOut_area_sum']['OUTPUT'],
            'JOIN': outputs['RefactorFields']['OUTPUT'],
            'JOIN_FIELDS': ['po'],
            'PREDICATE': [1],  # contains
            'SUMMARIES': [5],  # sum
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['JoinPo_box_sum'] = processing.run('qgis:joinbylocationsummary', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(7)
        if feedback.isCanceled():
            return {}

        # Join not_found_sum
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'INPUT': outputs['JoinPo_box_sum']['OUTPUT'],
            'JOIN': outputs['RefactorFields']['OUTPUT'],
            'JOIN_FIELDS': ['xf'],
            'PREDICATE': [1],  # contains
            'SUMMARIES': [5],  # sum
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['JoinNot_found_sum'] = processing.run('qgis:joinbylocationsummary', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(8)
        if feedback.isCanceled():
            return {}

        # Join no_info_sum
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'INPUT': outputs['JoinNot_found_sum']['OUTPUT'],
            'JOIN': outputs['RefactorFields']['OUTPUT'],
            'JOIN_FIELDS': ['xi'],
            'PREDICATE': [1],  # contains
            'SUMMARIES': [5],  # sum
            'OUTPUT': parameters['Joined_tracts_2016']
        }
        outputs['JoinNo_info_sum'] = processing.run('qgis:joinbylocationsummary', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Joined_tracts_2016'] = outputs['JoinNo_info_sum']['OUTPUT']
        return results

    def name(self):
        return 'tract_joins'

    def displayName(self):
        return 'tract_joins'

    def group(self):
        return ''

    def groupId(self):
        return ''

    def createInstance(self):
        return Tract_joins()

import os, sys
path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.
                                                       abspath(__file__))))
if path not in sys.path:
    sys.path.append(path)
from CM.CM_TUW32.N3scenario_to_raster import CalcEffectsAtRasterLevel
from CM.common_modules.readCsvData import READ_CSV_DATA
import CM.CEDM.modules.Subfunctions as SF
import CM.common_modules.cliprasterlayer as CRL
from CM.common_modules.exportLayerDict import export_layer as expLyr
from CM.CM_TUW1.read_raster import raster_array as RA


def main(input_raster_NUTS_id,
         input_raster_GFA_RES,
         input_raster_ENERGY_RES,
         input_raster_LAU2_id,
         input_raster_cp_share_1975,
         input_raster_cp_share_1990,
         input_raster_cp_share_2000,
         input_raster_cp_share_2014,
         output_raster_energy,
         output_csv_result):

    data_type = "f4"
    data_type_int = "uint32"
    local_input_dir = path + "/input_data"
    
    NUTS_id, gt = RA(input_raster_NUTS_id, dType=data_type_int, return_gt=True)
    GFA_RES = RA(input_raster_GFA_RES, dType=data_type)
    ENERGY_RES = RA(input_raster_ENERGY_RES, dType=data_type)
    LAU2_id = RA(input_raster_LAU2_id, dType=data_type_int)
    cp_share_1975 = RA(input_raster_cp_share_1975, dType=data_type)
    cp_share_1990 = RA(input_raster_cp_share_1990, dType=data_type)
    cp_share_2000 = RA(input_raster_cp_share_2000, dType=data_type)
    cp_share_2014 = RA(input_raster_cp_share_2014, dType=data_type)
    
    NUTS_id_size = NUTS_id.shape
    cp_share_2000_and_2014 = cp_share_2000 + cp_share_2014

    
    NUTS_RESULTS_ENERGY_BASE = READ_CSV_DATA(local_input_dir + "/RESULTS_SHARES_2012.csv", skip_header=3)[0]
    NUTS_RESULTS_ENERGY_FUTURE = READ_CSV_DATA(local_input_dir + "/RESULTS_SHARES_2030.csv", skip_header=3)[0]
    NUTS_RESULTS_ENERGY_FUTURE_abs = READ_CSV_DATA(local_input_dir + "/RESULTS_ENERGY_2030.csv", skip_header=3)[0]
    NUTS_RESULTS_GFA_BASE = READ_CSV_DATA(local_input_dir + "/RESULTS_GFA_2012.csv", skip_header=3)[0]
    NUTS_RESULTS_GFA_FUTURE = READ_CSV_DATA(local_input_dir + "/RESULTS_GFA_2030.csv", skip_header=3)[0]
    csv_data_table = READ_CSV_DATA(local_input_dir + "/Communal2_data.csv", skip_header=6)
    
    


    _, _ = CalcEffectsAtRasterLevel(NUTS_RESULTS_GFA_BASE,
                                    NUTS_RESULTS_GFA_FUTURE,
                                    NUTS_RESULTS_ENERGY_BASE,
                                    NUTS_RESULTS_ENERGY_FUTURE,
                                    NUTS_RESULTS_ENERGY_FUTURE_abs,
                                    NUTS_id,
                                    LAU2_id,
                                    cp_share_1975,
                                    cp_share_1990,
                                    cp_share_2000_and_2014,
                                    ENERGY_RES,
                                    GFA_RES,
                                    gt,
                                    NUTS_id_size,
                                    csv_data_table,
                                    output_raster_energy,
                                    output_csv_result)


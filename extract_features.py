import numpy as np
from frecuency_extraction import Frecuency_extraction
from temporal_extraction import Temporal_extract
from energy_extraction import Energy_signal
from get_data import get_data

class Extract_features(Frecuency_extraction,Temporal_extract,Energy_signal):
    pass


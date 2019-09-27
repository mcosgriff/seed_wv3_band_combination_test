import logging
import os.path

import numpy as np
import rasterio
from rasterio.enums import Compression

from enums import BandTable


class BandCombination:
    def __init__(self, raster_path: str, output_directory: str, band_combination_name: str):
        self.band_combination_name = band_combination_name
        self.raster_path = raster_path
        self.processed_raster = None
        self.logger = logging.getLogger('wv3_band_combination_processing')
        self.output_directory = output_directory

        np.seterr(divide='ignore', invalid='ignore')

    def __enter__(self):
        self.raster = rasterio.open(self.raster_path, mode='r', driver='GTiff')

    def __exit__(self, exc_type, exc_value, traceback):
        self.raster.close()

    def get_band_pixel_values(self, which_band: BandTable, array_type: str = 'float32') -> np.ndarray:
        band = self.raster.read(which_band.value)
        return band.astype(array_type)

    def which_bands_required(self) -> list:
        pass

    def process_band_combination(self) -> (np.ndarray, np.ndarray):
        red = self.get_band_pixel_values(self.which_band_at_index(0))
        green = self.get_band_pixel_values(self.which_band_at_index(1))
        blue = self.get_band_pixel_values(self.which_band_at_index(2))

        return red, green, blue

    def build_output_profile(self) -> property:
        profile = self.raster.profile
        profile.update(count=3, dtype=rasterio.float32, compress=Compression.packbits.value)

        return profile

    def save_output(self, red: np.ndarray, green: np.ndarray, blue: np.ndarray) -> str:
        if red.size > 0 and green.size > 0 and blue.size > 0:
            filename_without_extension = os.path.splitext(os.path.basename(self.raster_path))[0]
            output_path = os.path.join(self.output_directory,
                                       filename_without_extension + '_{}_{}.tif'.format(self.band_combination_name,
                                                                                        "processed"))
            with rasterio.open(output_path, mode='w', **self.build_output_profile()) as output:
                output.write_band(1, red)
                output.write_band(2, green)
                output.write_band(3, blue)

                return output.name

    def band_combination_name(self):
        return self.index_name

    def which_band_at_index(self, index: int) -> [BandTable, None]:
        bands = self.which_bands_required()

        if index > len(bands) or index < 0:
            return None

        return bands[index]


class GeneralLandCover(BandCombination):
    def __init__(self, raster_path: str, output_directory: str):
        BandCombination.__init__(self, raster_path, output_directory, 'general_land_cover')

    def which_bands_required(self) -> list:
        return [BandTable(8), BandTable(4), BandTable(6)]


class Water(BandCombination):
    def __init__(self, raster_path: str, output_directory: str):
        BandCombination.__init__(self, raster_path, output_directory, 'water')

    def which_bands_required(self) -> list:
        return [BandTable(8), BandTable(7), BandTable(6)]


class ExposedSoil(BandCombination):
    def __init__(self, raster_path: str, output_directory: str):
        BandCombination.__init__(self, raster_path, output_directory, 'exposed_soil')

    def which_bands_required(self) -> list:
        return [BandTable(5), BandTable(8), BandTable(4)]


class RoofingAndRoads(BandCombination):
    def __init__(self, raster_path: str, output_directory: str):
        BandCombination.__init__(self, raster_path, output_directory, 'roofing_and_roads')

    def which_bands_required(self) -> list:
        return [BandTable(5), BandTable(7), BandTable(8)]


class ArtificialFeaturesInDesert(BandCombination):
    def __init__(self, raster_path: str, output_directory: str):
        BandCombination.__init__(self, raster_path, output_directory, 'artificial_features_in_desert')

    def which_bands_required(self) -> list:
        return [BandTable(4), BandTable(1), BandTable(7)]

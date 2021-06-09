import logging
import shutil
from pathlib import Path

import pandas as pd
from tqdm import tqdm
import pytesseract
from PIL import Image


def main():
    LOGGING_FORMAT = '%(asctime)s %(levelname)s: %(message)s'
    DATE_FORMAT = '%Y%m%d %H:%M:%S'
    logging.basicConfig(filename='processing.log', level=logging.DEBUG, format=LOGGING_FORMAT, datefmt=DATE_FORMAT)

    common_words_path = Path('//home/maniac/Workspace/shoujin-all-in-order/traditional_Chinese_4808_common_words.csv')
    common_words = pd.read_csv(common_words_path)
    lookup_table = {}
    word_set = set()
    for i, _, word in common_words.values:
        lookup_table[word] = f'{i:05d}'
        word_set.add(word)

    source_root = Path('/home/maniac/Downloads/shoujin_all')
    target_root = Path('/home/maniac/Downloads/shoujin_all/temp')
    files = [file for file in source_root.glob('*')]
    for file in tqdm(files):
        with Image.open(file).convert('L') as image:
            recognized_string = pytesseract.image_to_string(image, lang='chi_tra')
            logging.debug(recognized_string)
            for c in recognized_string:
                if c in word_set:
                    index = lookup_table[c]
                    target_name = target_root / f'{index}.jpg'
                    logging.info(f'move file from {str(file)} to {str(target_name)}')
                    file.rename(target_name)
                    break


if __name__ == '__main__':
    main()

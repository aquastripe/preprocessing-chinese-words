from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

from tqdm import tqdm


class Word2Index(object):

    def __init__(self, common_words_file='traditional_Chinese_4808_common_words.csv'):
        self._word2index = {}
        common_words_dataframe = pd.read_csv(common_words_file)
        for row in common_words_dataframe.values:
            index = row[0]
            word = row[2]
            self._word2index[word] = f'{index:05d}'

    def __call__(self, word):
        return self._word2index[word]

    def keys(self):
        return self._word2index.keys()


def label_index():
    word2index = Word2Index()
    data_root = Path('/home/maniac/Downloads/shoujin_all')
    files = [file
             for file in data_root.iterdir()
             if file.suffix == '.jpg']
    print(files[:5])

    target_root = Path('/home/maniac/Downloads/shoujin_all/done')
    plt.ion()
    for file in tqdm(files):
        image = mpimg.imread(file)
        fig = plt.figure()
        plt.imshow(image)
        plt.show()
        s = input('> ')
        if s == '':
            print('Passed by user.')
            continue

        word = s[0]
        if word in word2index.keys():
            index = word2index(word)
            target_file = target_root / f'{index}.jpg'
            if target_file.exists():
                print(f'File {target_file} exists, passed.')
            else:
                file.rename(target_file)
                print(f'Moved from {str(file)} to {str(target_file)}.')
        else:
            print('Not found in dictionary, passed.')

        plt.close(fig)


if __name__ == '__main__':
    label_index()

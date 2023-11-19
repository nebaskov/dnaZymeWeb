import os
import pandas as pd


def convert_to_csv(filename: str, save_name: str) -> None:
    path = os.path.join(os.getcwd(), filename)
    ds = pd.read_excel(path)
    ds.to_csv(os.path.join(os.getcwd(), save_name), index=False)


if __name__ == '__main__':
    name1 = 'db_for_website.xlsx'
    name2 = 'candidates_1000gens.xlsx'
    convert_to_csv(name1, 'db.csv')
    convert_to_csv(name2, 'candidates.csv')

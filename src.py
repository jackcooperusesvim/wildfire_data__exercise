import pandas as pd
import numpy as np
import os


def xlsx_to_csv_recursive(root_dir):
    wdf = pd.DataFrame([])
    for dirpath, _, filenames in os.walk(root_dir):
        for file in filenames:
            if file.endswith(".xlsx"):
                xlsx_path = os.path.join(dirpath, file)
                csv_path = os.path.splitext(xlsx_path)[0] + ".csv"
                try:
                    # Read the file
                    df = pd.read_excel(xlsx_path)

                    # ------------------
                    # Concerning Headers
                    # ------------------

                    # Clean up headers

                    requires_second_header_parsing = False

                    if True:
                        headers = df.columns.to_series()
                        tl_filter = headers.str.contains("Unnamed")

                        requires_second_header_parsing = len(headers[tl_filter]) > 0

                        headers[headers.str.contains("Unnamed")] = np.nan
                        headers = headers.ffill()

                    if requires_second_header_parsing:
                        secondary_headers = df.iloc[0]
                        headers = headers + " - " + secondary_headers.fillna("")
                        headers = headers.str.removesuffix(" - ")

                    # get rid of the weird newline thing (GPT ftw with these regexes)
                    headers = (
                        headers.astype(str)
                        .str.replace(r"(\\n|\r\n|\r|\n)", "", regex=True)
                        .str.replace("/", "", regex=False)
                    )

                    # fix the few little headers which parsed weird
                    headers[headers == "Utility Name - Utility Name"] = "Utility Name"
                    headers = headers.str.replace("Utility Name - ", "Fire Start - ")
                    for i in ["Date", "Year", "Time"]:
                        headers = headers.str.replace(
                            f"^{i}$", "Fire Start - " + i, regex=True
                        )

                    df.columns = headers

                    # df.columns = ["--".join(map(str, col)) for col in df.columns]

                    # Files from some companies (*coughcoughsdgecoughcough**), have footers as well, placed one space under the lowest record, so we detect them by seeing if the whole second to last space is null, and removing those last two spaces if true

                    # Write to csv
                    # df.to_csv(csv_path, index=False)

                    wdf = pd.concat([wdf, df], axis=0)
                    print(f"Converted: {xlsx_path} -> {csv_path}")

                except Exception as e:
                    print(f"Failed to convert {xlsx_path}: {e}")
            first = False
    return wdf


def select_cols(df):
    cols = []
    for col in df:
        print(col)
        to_print = input(f"{col}? (y/any) :")
        if to_print == "y":
            cols.append(col)

    return cols


if __name__ == "__main__":
    root_directory = input("Enter the root directory to search: ").strip()
    xlsx_to_csv_recursive(root_directory)

import xlsxwriter

class ExcellGenerator:
    def generate_excel(self, keys_entities, result_entities):
        
        for i, res in enumerate(keys_entities):
            workbook = xlsxwriter.Workbook("{0}.xlsx".format(i))
            bold = workbook.add_format({'bold': True})
            merge_format = workbook.add_format({
                'bold': True,
                'border': 6,
                'align': 'center',
                'valign': 'vcenter',
                'fg_color': '#D7E4BC',

            })
            for j, r in enumerate(res):
                worksheet = workbook.add_worksheet(r.get("engine"))
                row = 0
                print(res)
                for u, url in enumerate(r.get("urls")):
                    # ws.merge_range(row, cl + 1, row, cl + 1, g.get("entities")[clss]["name"], merged_format)
                    worksheet.write(row, 0, "URL: ")
                    if(len(url.get("table")) > 0):
                        worksheet.merge_range(row, 1, row, len(url.get("table")[0]), url.get("url"), merge_format)
                        row += 1
                        worksheet.set_column(0, len(url.get("table")[0]), 30)
                        print(url.get("url"))
                        first = url.get("table")[0]
                        col = 0
                        for key in first:
                            worksheet.write(row, col, key, bold)
                            col += 1
                        row += 1
                        for t, table in enumerate(url.get("table")):
                            col = 0
                            for key in table:
                                if(col == 0 or col == 1):
                                    worksheet.write(row, col, table[key], bold)
                                else:
                                    worksheet.write(row, col, table[key])
                                col+=1
                            row += 1
                    else:
                        worksheet.merge_range(row, 1, row, 5, url.get("url"), merge_format)
                    row += 3
        workbook.close()
        return None
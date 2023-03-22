# import cv2
# import os
# import pyarrow as pa
# import pyarrow.parquet as pq
# import numpy as np
# from pdf_funcs import get_image_from_pdf
#
# from cv_funcs import OUTPUT_SIZE,process_img
#
# def write_image_to_parquet(img, filename):
#     img_np_arr = img.ravel()
#
#     try:
#         assert len(img_np_arr) == OUTPUT_SIZE[0] * OUTPUT_SIZE[1]
#     except Exception as e:
#         print('height, width', img.shape[:2])
#         print('I:', len(img_np_arr), OUTPUT_SIZE[0] * OUTPUT_SIZE[1])
#         raise e
#     # Set the path to the Parquet file
#     parquet_file = './data.parquet'
#
#     table = pa.Table.from_arrays(
#         [pa.array([i]) for i in img_np_arr],
#         schema=pa.schema([pa.field(str(i), pa.uint8()) for i in range(700 * 700)])
#     )
#
#     table.append_column('Label', pa.array(['FA'], pa.string()))
#     table.append_column('Filename', pa.array([filename], pa.string()))
#     # Check if the Parquet file already exists
#     if not os.path.exists(parquet_file):
#         # If the file does not exist, write the table to a new Parquet file
#         pq.write_table(table, parquet_file)
#     else:
#         # Should be done using this https://arrow.apache.org/docs/python/generated/pyarrow.parquet.write_to_dataset.html
#
#         with pq.ParquetWriter(parquet_file, table.schema) as writer:
#             writer.write_table(table)
#
#
# def create_parquet_dataset(label):
#     # Set the path to the directory containing the input PDF files
#     pdf_dir = f'../{label}/'
#
#     # Iterate over the PDF files in the input directory
#     dataset = []
#     filenames = []
#
#     # count = 0
#     for filename in os.listdir(pdf_dir):
#         if filename.endswith('.pdf'):
#             # Set the full path to the input and output files
#             pdf_path = os.path.join(pdf_dir, filename)
#             output_prefix = os.path.splitext(filename)[0]
#
#             img = get_image_from_pdf(pdf_path)
#
#             img = process_img(img)
#
#             img_np_arr = img.ravel()
#
#             filenames.append(output_prefix)
#
#             try:
#                 assert len(img_np_arr) == OUTPUT_SIZE[0] * OUTPUT_SIZE[1]
#             except Exception as e:
#                 print('height, width', img.shape[:2])
#                 print('I:', len(img_np_arr), OUTPUT_SIZE[0] * OUTPUT_SIZE[1])
#                 raise e
#
#             dataset.append(img_np_arr)
#             # count += 1
#             # if count > 1:
#             #     break
#
#     np_dataset = np.array(dataset)
#
#     rows, cols = np_dataset.shape[:2]
#
#     print(np_dataset.shape)
#
#     # Set the path to the Parquet file
#     parquet_file = f'./{label}.parquet'
#
#     table = pa.Table.from_arrays(
#         arrays=[pa.array(np_dataset[:, i]) for i in range(cols)],
#         schema=pa.schema([pa.field(str(i), pa.uint8()) for i in range(OUTPUT_SIZE[0] * OUTPUT_SIZE[1])])
#     )
#
#     table.append_column('Label', pa.array([label] * rows, pa.string()))
#     table.append_column('Filename', pa.array(filenames, pa.string()))
#     # Check if the Parquet file already exists
#     pq.write_table(table, parquet_file)
#
#
# if __name__ == '__main__':
#     # create_parquet_dataset('FA')
#     table2 = pq.read_table('normal.parquet')
#
#     print(table2.shape)
#     # print(table2[:3])
#
#     # Set the path to the directory containing the input PDF files
#     # label = 'normal'
#     # pdf_dir = f'../{label}/'
#     #
#     # # Iterate over the PDF files in the input directory
#     # count = 0
#     # for filename in os.listdir(pdf_dir):
#     #     if filename.endswith('.pdf'):
#     #         # Set the full path to the input and output files
#     #         pdf_path = os.path.join(pdf_dir, filename)
#     #         output_prefix = os.path.splitext(filename)[0]
#     #
#     #         img = get_image_from_pdf(pdf_path)
#     #
#     #         img = process_img(img)
#     #
#     #         write_image_to_parquet(img, output_prefix)
#     #         count += 1
#     #         if count > 2:
#     #             break
#     #
#     # table2 = pq.read_table('data.parquet')
#     #
#     # print(table2.shape)

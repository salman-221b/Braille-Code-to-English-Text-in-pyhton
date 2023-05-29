import numpy as np
import cv2
import math


BRAILLE_CODE_DICT = {'100000': 'A', '100001': 'B',
                     '110000': 'C', '111000': 'D', '101000': 'E',
                     '110001': 'F', '111001': 'G', '101001': 'H',
                     '010001': 'I', '011001': 'J', '100010': 'K',
                     '100011': 'L', '110010': 'M', '111010': 'N',
                     '101010': 'O', '110011': 'P', '111011': 'Q',
                     '101011': 'R', '010011': 'S', '011011': 'T',
                     '100110': 'U', '100111': 'V', '011101': 'W',
                     '110110': 'X', '111110': 'Y', '101110': 'Z'}

def eight_CCA():
    image = cv2.imread('Braille.png', 0)
    padded_image = np.pad(image, (1, 0), 'constant', constant_values=(0, 0))
    rows, cols = np.shape(padded_image)
    padded_image = (padded_image // 128)*255
    cv2.imshow("input image", padded_image)
    cv2.waitKey()

    label_matrix = np.zeros((rows, cols))

    label = 0
    equivalence_list = {}
    for i in range(1, rows):
        for j in range(1, cols):
            if padded_image[i][j] != 255:
                neighbor_labels = [label_matrix[i - 1][j - 1],
                                   label_matrix[i - 1][j],
                                   label_matrix[i - 1][j + 1],
                                   label_matrix[i][j - 1]]

                if all(l == 0 for l in neighbor_labels):
                    label += 1
                    label_matrix[i][j] = label
                    equivalence_list.update({label: label})
                else:
                    neighbor_labels = [l for l in neighbor_labels if l != 0]
                    min_label = min(neighbor_labels)
                    max_label = max(neighbor_labels)
                    equivalence_list.update({max_label: equivalence_list[min_label]})
                    label_matrix[i][j] = min_label

    for i in range(1, rows):
        for j in range(1, cols - 1):
            if label_matrix[i][j] != 0:
                label_matrix[i][j] = equivalence_list[label_matrix[i][j]]

    return label_matrix, rows, cols


def distance(p1, p2):
    _distance = math.sqrt((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2)
    return _distance


def minimum_distance_in_braille_image():
    label_matrix, rows, cols = eight_CCA()
    loop_len = len(np.unique(label_matrix)) - 1
    labels = np.unique(label_matrix)
    labels = np.delete(labels, [0])

    list_of_dot_cen = {}
    # loop to calculate centre of each object
    for i in range(0, loop_len):
        label_index = np.where(label_matrix == int(labels[i]))
        x_center = math.ceil(sum(label_index[0]) // len(label_index[0]))
        y_center = math.ceil(sum(label_index[1]) // len(label_index[1]))
        list_of_dot_cen.update({int(labels[i]): (x_center, y_center)})
    # print(list_of_dot_cen)

    min_dist = []
    for i in range(0, loop_len - 1):
        first_val = list_of_dot_cen[labels[i]]
        second_val = list_of_dot_cen[labels[i + 1]]
        min_dist.append(distance(first_val, second_val))
    min_dist = int(min(min_dist))

    return min_dist, label_matrix, rows, cols, list_of_dot_cen


def braille_to_english():
    min_dist, label_matrix, rows, cols, list_of_dot_cen = minimum_distance_in_braille_image()
    output_string = ""
    used_labels = []

    no_of_spaces = 0
    previousx = None
    for i in range(1, rows):
        for j in range(1, cols):
            if label_matrix[i][j] != 0 and label_matrix[i][j] not in used_labels:
                anti_check = "1"
                clock_check = "1"
                # print(padded_image[i][j])
                center = list_of_dot_cen[label_matrix[i][j]]
                currentx = center[1]
                if previousx is not None and abs(currentx-previousx) > 3*min_dist:
                    output_string += " "
                # so that we don't repeat the process for the same letter again
                used_labels.append(label_matrix[i][j])
                # for clockwise rotation
                if label_matrix[center[0]][center[1]+min_dist] != 0:
                    clock_check += '1'
                    used_labels.append(label_matrix[center[0]][center[1]+min_dist])
                else:
                    clock_check += '0'
                if label_matrix[center[0]+min_dist][center[1]+min_dist] != 0:
                    clock_check += '1'
                    used_labels.append(label_matrix[center[0]+min_dist][center[1]+min_dist])

                else:
                    clock_check += '0'
                if label_matrix[center[0]+(2*min_dist)][center[1]+min_dist] != 0:
                    clock_check += '1'
                    used_labels.append(label_matrix[center[0]+(2*min_dist)][center[1]+min_dist])

                else:
                    clock_check += '0'
                if label_matrix[center[0]+(2*min_dist)][center[1]] != 0:
                    clock_check += '1'
                    used_labels.append(label_matrix[center[0]+(2*min_dist)][center[1]])
                else:
                    clock_check += '0'
                if label_matrix[center[0]+min_dist][center[1]] != 0:
                    clock_check += '1'
                    used_labels.append(label_matrix[center[0]+min_dist][center[1]])
                else:
                    clock_check += '0'

                # For anti-clockwise rotation
                if label_matrix[center[0]][center[1]-min_dist] != 0:
                    anti_check += '1'
                    used_labels.append(label_matrix[center[0]][center[1]-min_dist])

                else:
                    anti_check += '0'
                if label_matrix[center[0]+min_dist][center[1]-min_dist] != 0:
                    anti_check += '1'
                    used_labels.append(label_matrix[center[0]+min_dist][center[1]-min_dist])

                else:
                    anti_check += '0'
                if label_matrix[center[0]+(2*min_dist)][center[1]-min_dist] != 0:
                    anti_check += '1'
                    used_labels.append(label_matrix[center[0]+(2*min_dist)][center[1]-min_dist])

                else:
                    anti_check += '0'
                if label_matrix[center[0]+(2*min_dist)][center[1]] != 0:
                    anti_check += '1'
                    used_labels.append(label_matrix[center[0]+(2*min_dist)][center[1]])

                else:
                    anti_check += '0'
                if label_matrix[center[0]+min_dist][center[1]] != 0:
                    anti_check += '1'
                    used_labels.append(label_matrix[center[0]+min_dist][center[1]])

                else:
                    anti_check += '0'

                # checking if anti-clockwise rotation was right or clockwise
                if clock_check >= anti_check:
                    previousx = center[1]+min_dist
                    output_string += BRAILLE_CODE_DICT[clock_check]
                else:
                    previousx = center[1]
                    rotated_string = anti_check[2:] + anti_check[:2]
                    reversed_string = rotated_string[::-1]
                    output_string += BRAILLE_CODE_DICT[reversed_string]

    return output_string


english_output = braille_to_english()
newline = 0
print("English Output: ")
for i in range(0, len(english_output)):
    print(english_output[i], end='')
    if english_output[i] == " ":
        newline += 1
    if newline > 17:
        print('\n')
        newline = 0

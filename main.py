import cv2


def get_tuples(img):

    # convert the input image to grayscale->black & white + a flip
    grayImage = cv2.flip(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY), 0)
    (thresh, img) = cv2.threshold(grayImage, 127, 255, cv2.THRESH_BINARY)

    # cv2.imshow('image', img)
    # cv2.waitKey(0)

    row, col = img.shape

    local_tops = []
    local_tops_unique = []

    # Iterate through the Image columns, goal is to get the maximum segments
    for j in range(col):
        local_max = 1
        for i in range(row):
            # value at current element different from previous -> new segment
            if i != 0 and img[i][j] != img[i - 1][j]:
                local_max += 1

        if not local_tops_unique.__contains__(local_max):
            local_tops_unique.append(local_max)

        local_tops.append(local_max)

    # Init the tuple array with default 0s.
    output_tuples = []
    tuple_idx_starts: dict = dict()

    for top in local_tops_unique:
        tuple_idx_starts[top] = len(output_tuples)
        for i in range(top):
            output_tuples.append([0] * col)

    # Set the exact values for each segment
    for j in range(col):
        tupple_index = 0
        cur_val = 0
        for i in range(row):
            start_idx = tuple_idx_starts[local_tops[j]]

            # same segment, continue
            if i == 0 or img[i][j] == img[i - 1][j]:
                cur_val += 1
                output_tuples[start_idx + tupple_index][j] = cur_val

            # new segment, reset values, increment index
            if i != 0 and img[i][j] != img[i - 1][j]:
                cur_val = 1
                tupple_index += 1
                output_tuples[start_idx + tupple_index][j] = cur_val

    return output_tuples


def setSQL(tuples):

    # building base table
    base = "with tuples as (\n\t SELECT"
    for i in range(len(tuples)):
        cur_string = "ARRAY_CONSTRUCT("
        if i != 0:
            cur_string = ", " + cur_string

        for j in range(len(tuples[0])):
            cur_string = cur_string + str(tuples[i][j])

            if j != len(tuples[0]) - 1:
                cur_string = cur_string + ", "

        cur_string = "\n\t\t" + cur_string + ") as span" + str(i)
        base = base + cur_string

    base = base + "\n)\n,"

    # row table
    rows = ""
    for i in range(len(tuples)):
        cur_string = "\nrow" + str(i) + " AS (SELECT index, value FROM TABLE(FLATTEN(input=> SELECT span" + str(i) + " FROM tuples)))"
        if i != 0:
            cur_string = ", " + cur_string

        rows = rows + cur_string

    # joins
    rows_pre = "\n\nSELECT row0.index,"
    for i in range(len(tuples)):
        cur_string = "\n\trow" + str(i) + ".value as value_" + str(i)
        if i != 0:
            cur_string = ", " + cur_string
        rows_pre = rows_pre + cur_string

    rows_post = "\nfrom row0"
    for i in range(1, len(tuples)):
        cur_string = "\nLEFT JOIN row" + str(i) + " ON row0.index = row" + str(i) + ".index"
        rows_post = rows_post + cur_string

    # concat all, single string output
    return base + rows + rows_pre + rows_post


if __name__ == "__main__":
    originalImage = cv2.imread('./main.png')
    tuples = get_tuples(originalImage)
    sql_string = setSQL(tuples)
    print(sql_string)

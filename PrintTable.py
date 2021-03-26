import math

font_colors = ['\033[91m', '\033[92m', '\033[93m', '\033[95m']
font_reset = '\033[0m'
font_bold ='\033[1m'

def print_table(data, col_width, highlite):

    count_rows = len(data)

    if count_rows == 0:
        print("Data is empty")
        return 

    #  HEADER / Top border

    rf = []
    row_content = []

    for k, v in data[0].items():
        if isinstance(v, dict):
            w = col_width*len(v) + (len(v)-1)
            rf.append("{:^"+str(w)+"}")
            row_content.append("═"*w)
        else:
            rf.append("{:^"+str(col_width)+"}")
            row_content.append("═"*col_width)

    row_format ="{:^1}".join(rf)
    row_format = "{:^1}"+row_format+"{:^1}"

    row_content = sum([[i, "╦"] for i in row_content], [])[:-1]
    row_content.insert(0,"╔")
    row_content.append("╗")

    print(row_format.format(*row_content))

    #  HEADER / First row

    row_content = []

    for k, v in data[0].items():
        if isinstance(v, dict):
            spaces = col_width*len(v) + (len(v)-1) - len(k)
            spaces_l = math.floor(spaces/2)
            row_content.append(" "*spaces_l+font_bold+str(k)+font_reset+" "*(spaces-spaces_l))
        else:
            row_content.append(" ")

    row_content = sum([[i, "║"] for i in row_content], [])[:-1]
    row_content.insert(0,"║")
    row_content.append("║")

    print(row_format.format(*row_content))

   #  HEADER / Second row

    row_format = "{:^1}"
    row_content = []
    row_content.insert(0,"║")

    for k, v in data[0].items():
        if isinstance(v, dict):
            tmp_content = []
            tmp_format = []
            w = col_width*len(v) + (len(v)-1)
            for kk, vv in v.items():
                spaces = col_width - len(kk)
                spaces_l = math.floor(spaces/2)
                tmp_content.append(" "*spaces_l+font_bold+str(kk)+font_reset+" "*(spaces-spaces_l))
                tmp_format.append("{:^"+str(col_width)+"}")
            tmp_content = sum([[i, "│"] for i in tmp_content], [])[:-1]
            for tc in tmp_content:
                row_content.append(tc)
            row_content.append("║")
            row_format += "{:^1}".join(tmp_format)
            row_format += "{:^1}"
        else:
            row_content.append(k)
            row_content.append("║")
            row_format += "{:^"+str(col_width)+"}"
            row_format += "{:^1}"

    print(row_format.format(*row_content))

    #  HEADER / Bottom border

    row_content = []
    row_content.insert(0,"╠")

    for k, v in data[0].items():
        if isinstance(v, dict):
            tmp_content = []
            w = col_width*len(v) + (len(v)-1)
            for kk, vv in v.items():
                tmp_content.append("═"*col_width)
            tmp_content = sum([[i, "╪"] for i in tmp_content], [])[:-1]
            for tc in tmp_content:
                row_content.append(tc)
            row_content.append("╬")
        else:
            row_content.append("═"*col_width)
            row_content.append("╬")
    row_content[-1] = "╣"

    print(row_format.format(*row_content))

    #  BODY / Data row

    for i, row in enumerate(data):

        row_content = []
        row_content.insert(0,"║")
        row_content_bottom = []
        row_content_bottom.insert(0,"╠")
        row_content_end = []
        row_content_end.insert(0,"╚")

        for k, v in row.items():
            if isinstance(v, dict):
                tmp_content = []
                tmp_content_bottom = []
                tmp_content_end = []
                w = col_width*len(v) + (len(v)-1)
                for kk, vv in v.items():
                    if vv in highlite:
                        spaces = col_width-len(vv)
                        spaces_l = math.floor(spaces/2)
                        tmp_content.append(" "*spaces_l+font_colors[highlite.index(vv)]+str(vv)+font_reset+" "*(spaces-spaces_l))
                    else:
                        tmp_content.append(vv)
                    tmp_content_bottom.append("─"*col_width)
                    tmp_content_end.append("═"*col_width)
                tmp_content = sum([[i, "│"] for i in tmp_content], [])[:-1]
                tmp_content_bottom = sum([[i, "┼"] for i in tmp_content_bottom], [])[:-1]
                tmp_content_end = sum([[i, "╩"] for i in tmp_content_end], [])[:-1]
                for tc in tmp_content:
                    row_content.append(tc)
                for tcb in tmp_content_bottom:
                    row_content_bottom.append(tcb)
                for tce in tmp_content_end:
                    row_content_end.append(tce)
                row_content.append("║")
                row_content_bottom.append("╬")
                row_content_end.append("╩")
            else:
                row_content.append(v)
                row_content.append("║")
                row_content_bottom.append("─"*col_width)
                row_content_bottom.append("║")
                row_content_end.append("═"*col_width)
                row_content_end.append("╩")
        row_content[-1] = "║"
        row_content_bottom[-1] = "╣"
        row_content_end[-1] = "╝"
        print(row_format.format(*row_content))
        if i < len(data)-1:
            print(row_format.format(*row_content_bottom))
        else:
            print(row_format.format(*row_content_end))

# data = [
#     {"foot_L":{"mark":"CS", "OPF":0.2}, "foot_R":{"mark":"CE", "OPF":0.2}},
#     {"foot_L":{"mark":"C", "OPF":0.2}, "foot_R":{"mark":"F", "OPF":0}},
#     {"foot_L":{"mark":"C", "OPF":0.2}, "foot_R":{"mark":"F", "OPF":0}},
#     {"foot_L":{"mark":"C", "OPF":0.2}, "foot_R":{"mark":"F", "OPF":0}}
# ]


# print_table(data, 7)

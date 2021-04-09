font_colors = ['\033[91m', '\033[92m', '\033[93m', '\033[95m']
font_reset = '\033[0m'
font_bold ='\033[1m'

def floor(n):
    res = int(n)
    return res if res == n or n >= 0 else res-1

def pt_spaces(string, width, highlite, bold):
    spaces = width - len(string)
    spaces_l = floor(spaces/2)
    spaces_r = spaces-spaces_l
    output = " "*spaces_l+string+" "*spaces_r
    if string in highlite:
        output = font_colors[highlite.index(string)]+output+font_reset
    if bold is True:
        output = font_bold+output+font_reset
    return output

def print_table(data, highlite):

    index_colWidth = 3

    # data = [
    #     {"foot_L":{"mark":"CS", "OPF":0.2, "transf":{"loc":[0,0,0], "rot":[0.4,0.4,0,4], "scale":[0.9,0.9,0.9]} }, "foot_R":{"mark":"CE", "OPF":0.3, "transf":None} },
    #     {"foot_L":{"mark":"C", "OPF":0.22, "transf":None}, "foot_R":{"mark":"F", "OPF":0, "transf":None} },
    #     {"foot_L":{"mark":"C", "OPF":0.222, "transf":None}, "foot_R":{"mark":"F", "OPF":0, "transf":None} },
    #     {"foot_L":{"mark":"C", "OPF":0.22222222, "transf":None}, "foot_R":{"mark":"F", "OPF":0, "transf":{"loc":[0,0,0], "rot":[0.4,0.4,0,4], "scale":[0.9,0.9,0.9]} } }
    # ]

    ################################################################# Get column widths

    col_width = {}# {"column name":length}
    for i, row in enumerate(data):# Iterate all items
        for k, v in row.items():# Iterate each item keys and values
            if isinstance(v, dict):# if value is dict
                for kk, vv in v.items():# Iterate each value for sub-level keys and values
                    key_len = len(str(kk))# Key name length
                    value_len = len(str(vv))# Value lenght
                    # Set longer as max length
                    max_len = key_len
                    if isinstance(vv, dict) == False:
                        if value_len > key_len:
                            max_len = value_len
                    else:# If value is dict
                        for kkk, vvv in vv.items():# Iterate sub-sub-level
                            string = str(vvv)
                            item_len = len(string) 
                            if max_len < item_len:
                                max_len = item_len 
                    if kk in col_width:# Update col_width dict new max_len
                        if col_width[kk] < max_len:
                            col_width[kk] = max_len
                    else:# If not existing create item in col_width
                        col_width[kk]=max_len


    ################################################################# Print table header

    rows = []# Rows for printing
    L1_section=[]# Collect top level data
    L2_section = []# Collect sub-level data
    L1_border_top = []# Collect cells border top
    L2_border_bottom = []# Collect cells border bottom
    # Index
    L1_section.append(" "*index_colWidth)
    L2_section.append(" "*index_colWidth)
    L1_border_top.append("═"*index_colWidth)
    L2_border_bottom.append("═"*index_colWidth)
    for k, v in data[0].items():# Get keys only from first entry
        # Width for top level cells
        width = len(col_width)-1
        for kk,vv in col_width.items():
            width += vv
        L1_section.append(pt_spaces(k, width, highlite,True))# Make data for top level cell
        L1_border_top.append("═"*width)# Make top level cell upper border
        L2_cells = []# Reset collection of sub-level data
        L2_cells_bottom = []# Reset collection of sub-level bottom borders
        for kk, vv in v.items():# Sub-level
            width = col_width[kk]# Get cell width
            L2_cells.append(pt_spaces(kk, width, highlite,True))# Make data for sub-level cell
            L2_cells_bottom.append("═"*width)# Make sub-level cell bottom border
        L2_section.append("│".join(L2_cells))# Join section sub-level data
        L2_border_bottom.append("╪".join(L2_cells_bottom))# Join section sub-level bottom borders
    rows.append("╔"+"╦".join(L1_border_top)+"╗")
    rows.append("║"+"║".join(L1_section)+"║")
    rows.append("║"+"║".join(L2_section)+"║")
    rows.append("╠"+"╬".join(L2_border_bottom)+"╣")
    print( "\n".join(rows) )

    
    ################################################################# Print table body

    rows = []# Rows for printing
    row_separator=[]
    for i, row in enumerate(data):# Iterate data items
        # Check for row_lines, sub-sub levels will be splited in multiple lines
        row_lines = 1# Init is 1 row
        for k, v in row.items():# Top level
            if isinstance(v, dict):# Must be dict
                for kk, vv in v.items():# Sub Level
                    if isinstance(vv, dict):# Must be dict
                        dict_len = len(vv)# Get sub-sub level dict length
                        if row_lines < dict_len:# If bigger then previous expand row height
                            row_lines = dict_len

        row_single = []# Reset single row
        row_separator = ""
        bottom_border = ""
        for li in range(1,row_lines+1):# Iterate row height to add lines per single row for values splited to multiple rows
            section = []# Reset section
            if row_separator == "":# Declare it first time
                section_row_separator = []
                section_bottom_border = []
                # Add index separator and bottom border
                section_row_separator.append("─"*index_colWidth)
                section_bottom_border.append("═"*index_colWidth)
            for k, v in row.items():# Top Level
                if isinstance(v, dict):# Value must be dict
                    cells = []# Reset section cells
                    if row_separator == "":# Declare it first time
                        cells_separator = []
                        cells_bottom_border = []
                    for kk, vv in v.items():# Sub-level
                        string = " "# Default is empty value
                        if li == 1:# For first line always get value
                            string = str(vv)
                        if isinstance(vv, dict):# If value is dict use sub-sub-level at index as same as line is
                            if len(vv) >= li:# Check if index exists
                                value = list(vv.items())[li-1:li]# Slice from dict
                                string = str(value[0][1])
                        width = col_width[kk]
                        cells.append(pt_spaces(string, width, highlite, False))# Make data for sub level
                        if row_separator == "":# Declare it first time
                            # Add borders for data cells
                            cells_separator.append("─"*width)
                            cells_bottom_border.append("═"*width)
                    section.append("│".join(cells))# Join section
                    if row_separator == "":# Declare it first time
                        section_row_separator.append("┼".join(cells_separator))
                        section_bottom_border.append("╩".join(cells_bottom_border))
            index = " "*index_colWidth
            if li == 1:
                index = pt_spaces(str(i+1), index_colWidth, highlite, False)
            row_single.append("║"+index+"║"+"║".join(section)+"║")# Join section lines into single row output
            if row_separator == "":# Declare it first time
                row_separator = "\n"+"╠"+"╬".join(section_row_separator)+"╣"+"\n"
                bottom_border = "\n"+"╚"+"╩".join(section_bottom_border)+"╝"
        rows.append("\n".join(row_single))# Add single row to rows
    print( row_separator.join(rows)+bottom_border )

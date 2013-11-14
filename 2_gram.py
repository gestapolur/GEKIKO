# run on python3
# fi = open("test.in","r")
fi = open("zojuan.txt", "r")
char_cnt = dict()

p = dict()

word_time_distr = dict() # word appear times : word cnt

def is_zh_char(c):
    # print(c, len(c))
    try:
        assert 19968 <= ord(c) <= 40908
        return True
    except:
        return False


def init():
    global total_char, total_two_chars
    total_two_chars = 0
    total_char = 0
    for line in fi:
        prev = ''
        for c in line:
            if is_zh_char(c):
                try:
                    char_cnt[c] += 1
                except KeyError:
                    total_char += 1
                    char_cnt[c] = 1
                if prev and is_zh_char(prev):
                    try:
                        char_cnt[tuple([prev, c])] += 1
                    except KeyError:
                        total_two_chars += 1
                        char_cnt[tuple([prev, c])] = 1
                prev = c
            else:
                prev = ''


def cal():
    global average_use_time
    for k, v in char_cnt.items():
        if isinstance(k, str):
            p[ k ] = float(v) / float(total_char)
        else:
            p[ k ] = float(v) / float(total_two_chars)

    # word appear time distribution count
    for k, v in char_cnt.items():
        if isinstance(k, tuple):
            try:
                word_time_distr[v] += 1
            except KeyError:
                word_time_distr[v] = 1

    average_use_time = 0
    for k, v in word_time_distr.items():
        average_use_time += k*v
    print(average_use_time, total_two_chars)
    average_use_time = float(average_use_time) / float(total_two_chars)
    print("average use time:", average_use_time)


def out():
    out = open("test.out", "w")
    print(total_char, total_two_chars)
    # print('character probability:')
    for k in sorted(p, key=lambda x: p[x], reverse=True):
        if isinstance(k, tuple):
            #print(k, p[k])
            out.write("%s %s\n" % (k, p[k]))

    out = open("distr.out", "w")
    out.write("{")
    for k, v in word_time_distr.items():
        out.write("{%s., %s.}," % (k, v))
    out.write("}\n")
    out.close()

    out = open("graph.out", "w")
    out.write("{")
    print(len(char_cnt))
    for k, v in char_cnt.items():
        if isinstance(k, tuple) and v > average_use_time:
            out.write('"%s"->"%s", ' % (k[0], k[1]))
    out.write("}\n")
    out.close()

init()

# for v in sorted(char_cnt, key=lambda x: char_cnt[x]):
#     print(v, char_cnt[v])

cal()

out()

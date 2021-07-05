import re
import book
file = input('please enter the name of the file: ')
with open(file, 'r') as f:
    read_data = f.readlines()

outputfile = '_'.join(['book',file.split('_')[1]])

with open(outputfile, 'w') as f:
    f.write("timestamp,id,side,action,price,quantity,bp0,bq0,bp1,bq1,bp2,bq2,bp3,bq3,bp4,bq4,ap0,aq0,ap1,aq1,ap2,aq2,ap3,aq3,ap4,aq4,bv,bq,av,aq\n")
    for i in range(1, len(read_data)):
        t,s,a,id,p,q = re.findall(r'(.+)\n',read_data[i])[0].split(',')
        row = book.row_data(int(t), s,a, int(id), int(p), int(q))
        bk = book.book(row)
        f.write(f"{row.t},{row.id},{row.s},{row.a},{row.p},{row.q},{bk.top[0]},{bk.p_to_q('b',bk.top[0])},{bk.top[1]},{bk.p_to_q('b',bk.top[1])},{bk.top[2]},{bk.p_to_q('b',bk.top[2])},{bk.top[3]},{bk.p_to_q('b',bk.top[3])},{bk.top[4]},{bk.p_to_q('b',bk.top[4])},{bk.bottom[0]},{bk.p_to_q('a',bk.bottom[0])},{bk.bottom[1]},{bk.p_to_q('a',bk.bottom[1])},{bk.bottom[2]},{bk.p_to_q('a',bk.bottom[2])},{bk.bottom[3]},{bk.p_to_q('a',bk.bottom[3])},{bk.bottom[4]},{bk.p_to_q('a',bk.bottom[4])},{bk.bv},{bk.bq},{bk.av},{bk.aq}\n")
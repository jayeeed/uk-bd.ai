

def WholeSentence(context, w_indx_s, w_indx_e):
    w_indx_e -= 1
    # print(context[w_indx_s])
    # print(context[w_indx_e])
    sz = len(context)

    while True:

        if w_indx_e < sz and context[w_indx_e] != '.':
            w_indx_e += 1

        else:
            break

    while True:

        if w_indx_s >= 0 and context[w_indx_s] != '.':
            w_indx_s -= 1
           # print(context[w_indx_s])

        else:
            break

    sentence = ''
    w_indx_s += 1
    while w_indx_s <= w_indx_e:
        sentence += context[w_indx_s]
        w_indx_s += 1
    return sentence


# cntxt = "IPSITA COMPUTERS PTE LTD was founded in the year of 1994.Services of IPSITS are Software and Web application development. IPSITA has experience of More than 25 years.The address of ipsita is Level 7,25/A Green Road,Dhaka-1205,Bangladesh.The founder of ipsita is Md. Atique Ullah Siddique.The contact number of ipsita is '+8801000000000'.color of the sky is blue."
# print(WholeSentence(cntxt, 262, 287))

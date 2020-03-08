import numpy as np


# Viterbi algorithm

def viterbi(A, C, B, Obs_seq):
    no_of_states = A.shape[0]  # number of states
    no_of_sequence = Obs_seq.shape[1]  # length of observation sequence

    # initialize D and E matrices
    D = np.zeros([no_of_states, no_of_sequence])
    E = np.zeros([no_of_states, no_of_sequence - 1])
    D[:, 0] = np.multiply(C, B[:, 0])


    # compute D and E in a nested loop
    for n in range(1, no_of_sequence):
        for i in range(no_of_states):
            temp_product = np.multiply(A[:, i], D[:, n - 1])
            D[i, n] = np.amax(temp_product) * B[i, Obs_seq[0, n] - 1]
            E[i, n - 1] = np.argmax(temp_product)



    max_ind = np.zeros([1, no_of_sequence])
    max_ind[0, -1] = np.argmax(D[:, -1])

    # Backtracking
    for n in range(no_of_sequence - 2, 0, -1):
        max_ind[0, n] = E[int(max_ind[0, n + 1]), n]

    # Convert zero-based indices to state indices
    S_opt = max_ind.astype(int) + 1


    probabilty=np.ones(no_of_sequence)
    for ix, iy in np.ndindex(D.shape):
        if(ix==0):
         probabilty[iy]=(D[ix,iy])
        else:
            if(D[ix,iy]>probabilty[iy]):
                probabilty[iy]=D[ix,iy]


    return S_opt,probabilty



# Define model parameters

if __name__ == "__main__":

    A = np.array([[0.3777,0.0110,0.0009,0.0084,0.0584,0.0090,0.0025],
                  [0.0008,0.0002,0.7968,0.0005,0.0008,0.1698,0.0041],
                  [0.0322,0.0005,0.0050,0.0837,0.0615,0.0514,0.2231],
                  [0.0366,0.0004,0.0001,0.0733,0.4509,0.0036,0.0036],
                  [0.0096,0.0176,0.0014,0.0086,0.1216,0.0177,0.0068],
                  [0.0068,0.0102,0.1011,0.1012,0.0120,0.0728,0.0479],
                  [0.1147,0.0021,0.0002,0.2157,0.4744,0.0102,0.0017]])


    C = np.array([[0.2767, 0.0006, 0.0031,0.0453,0.0449,0.0510,0.2026]])



    B = np.array([[0.000032,0.0,0.0,0.000048,0.0],
                  [0.0,0.308431,0.0,0.0,0.0],
                  [0.0,0.000028,0.000672,0.0,0.000028],
                  [0.0,0.0,0.000340,0.0,0.0],
                  [0.0,0.000200,0.000233,0.0,0.002337],
                  [0.0,0.0,0.010446,0.0,0.0],
                  [0.0,0.0,0.0,0.506099,0.0]])


    observation_seq_dic={
      "janet":1,
      "will":2,
      "back":3,
      "the":4,
      "bill":5
    }

    tag_seq_dic={
          "1":"NNP",
          "2":"MD",
          "3":"VB",
          "4":"JJ",
          "5":"NN",
          "6":"RB",
          "7":"DT"
    }


    mysentance=input("enter a sentance:")
    # mysentance="Janet will back the bill"
    mysentance=mysentance.split()
    Obs_seq_words=[[]]
    for word in mysentance:
        Obs_seq_words[0].append(observation_seq_dic.get(word.lower()))

    Obs_seq = np.stack(np.array(Obs_seq_words))
    # print(Obs_seq)

    # Apply Viterbi algorithm
    S_opt,probabilty = viterbi(A, C, B, Obs_seq)

    print('Observation sequence:   '+str(mysentance))
    print("----------------------------------------")

    optimal_tag_seq=[]
    for i in np.nditer(S_opt):
        optimal_tag_seq.append(tag_seq_dic.get(str(i)))

    print("Optimal tag sequence:  "+str(optimal_tag_seq))
    print("----------------------------------------")

    print("probabilty at each state is :"+str(probabilty))
    print("----------------------------------------")

    print("final probabilty:" + str(probabilty[-1]))
    print("#############################################")

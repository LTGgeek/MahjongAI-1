from collections import defaultdict
import numpy

class MahjongAgent:
    wan = [1,1,3,1,2,3,0,0,1]  #0-8
    so = [0,0,0,1,0,0,0,2,1]   #9-17
    pin = [1,1,0,1,0,0,0,0,0]  #18-26
    honor = [0,0,0,0,0,0,0]
    hands = [wan,so,pin]
    partition = {}
    efficiency_map = {}
    
    # sequence_two-way * 0.7 * 0.24
    # sequence_middle * 0.01
    # def new_partition(self):
    #     pair = []
    #     for t in self.hands:
    #         sequence = {}
    #         triplet = {}
    #         kang_triplet = []
    #         for x in range(len(t)):
    #             if(t[x] == 4):
    #                 # mark index as kang_triplet
    #                 kang_triplet.append(x)
    #             if(t[x] == 3):
    #                 # mark index as triplet
    #                 print("triplet at:" + str(x))
    #                 triplet.update(str(x),x)
    #             elif(t[x] == 2):
    #                 # mark index as pair
    #                 print("pair at:" + str(x))
    #                 pair.append(x) 
    #             elif(x<=6):
    #                 if(t[x] >= 1 and t[x+1]>=1 and t[x+2]>=1):
    #                     true_count = 0
    #                     if(t[x] >= 3):
    #                         true_count += 1
    #                     if(t[x] >= 3):
    #                         continue
    #                     else:
    #                         # mark index as sequence-complete
    #                         print("sequence complete at:" + str(x))
    #                         sequence.update(str(x),x)
                
    #         for num in sequence:
    #             if (sequence.get(num) in triplet or sequence.get(num+1) in triplet or sequence(num+2) in triplet):
    #                 # mark sequence index with triplet overlap
                    
    #                 print("sequence complete plus pair")
            
    def tenpai_status_check(self,hand):
        return_list = {}
        single_tile = []
        if(len(hand)%3 == 1):
            return return_list

        if(len(hand) == 14):
            # check seven-pairs
            pair_count = 0
            x = 0
            while x < 13:
                if(hand[x] == hand[x+1]):
                    pair_count += 1
                    x += 2
                else:
                    single_tile.append(hand[x])
                    x += 1
            if(x == 13):
                single_tile.append(hand[x])

            if(pair_count == 7):
                for tile in hand:
                    return_list.setdefault(tile,tile)
                return return_list
            
            if(pair_count == 6):
                return_list.setdefault(single_tile[0],single_tile[1])
                return_list.setdefault(single_tile[1],single_tile[0])
                return return_list

        if(len(hand) == 2):
            return_list.setdefault(hand[0],hand[1])
            return_list.setdefault(hand[1],hand[0])
            return return_list
        
        if(len(hand) == 3):
            if(hand[0]//9 == hand[1]//9 and hand[1] - hand[0] <= 2):
                if(hand[1] - hand[0] == 2):
                    # sequence-middle
                    return_list.setdefault(hand[2],hand[1]-1)
                else:
                    # two-way or one-way
                    temp_list = []
                    left = hand[0] - 1
                    right = hand[1] + 1
                    if(left//9 == right//9):
                        # two-way
                        temp_list.append(left)
                        temp_list.append(right)
                        return_list.setdefault(hand[2],temp_list)
                    else:
                        # one-way
                        if(left%8 > right%8):
                            return_list.setdefault(hand[2],left)
                        else:
                            return_list.setdefault(hand[2],right)

            if(hand[1]//9 == hand[2]//9 and hand[2]-hand[1] <= 2):
                if(hand[2] - hand[1] == 2):
                    # sequence-middle
                    return_list.setdefault(hand[0],hand[2]-1)
                else:
                    # two-way or one-way
                    temp_list = []
                    left = hand[1] - 1
                    right = hand[2] + 1
                    if(left // 9  == right // 9):
                        # two-way
                        temp_list.append(left)
                        temp_list.append(right)
                        return_list.setdefault(hand[0],temp_list)
                    else:
                        # one-way
                        if(left % 8 > right % 8):
                            temp_list.append(left)
                        else:
                            temp_list.append(right)
                            return_list.setdefault(hand[0],temp_list)

        if(len(hand) == 5):
            remain = []
            for x in range(len(hand)-2):
                remain = self.seq_extract(hand,x)
                remain = self.pair_extract(remain)
                remain = self.tri_extract(remain)
                if(len(remain) != 5):
                    if(len(remain) == 1):
                        temp_list = []
                        y = 0
                        while y < len(hand):
                            if(hand[y] != remain[0]):
                                temp_list.append(hand[y])
                                y+=2
                            y+=1
                        return_list.setdefault(remain[0],temp_list)
                    # print("check point 1")
                    return_list.update(self.tenpai_status_check(remain))


        if(len(hand) > 5):
            # print("greater 5")
            remain = []
            for x in range(len(hand)-2):
                remain = self.seq_extract(hand,x)
                remain = self.tri_extract(remain)
                if(len(remain) < len(hand)):
                    # print("check point 2")
                    return_list.update(self.tenpai_status_check(remain))
        
        # print("final:")
        return return_list
          
    
    def pair_extract(self,hand):
        remain = []
        x = 0
        while x < (len(hand)-1):
            if (hand[x] == hand[x+1]):
                x+=2
                continue
            remain.append(hand[x])
            x+=1
        if(x<len(hand)):
            remain.append(hand[x])
        # print("extract pair:")
        # print(remain)
        return remain 
    


    def tri_extract(self,hand):  
        remain = []
        x = 0
        while x < (len(hand)-2):
            if(hand[x] == hand[x+1] == hand[x+2]):
                x+=3
                continue
            remain.append(hand[x])
            x+=1

        if(x<len(hand)):
            remain.append(hand[x])
        if(x<len(hand)-1):
            remain.append(hand[x+1])

        # print("extract tri:")
        # print(remain)
        return remain

    def seq_extract(self,hand,index):

        remain = []
        remain.extend(hand[0:index])
        partial_hand = hand[index:]
        index_1_count = 0
        index_2_count = 0
        index_3_count = 0
        index_1_move = 0
        index_2_move = 0
        index_3_move = 0
        x = 0
        value = partial_hand[0]
        while x < (len(partial_hand)-2):
            
            #print(partial_hand)
            if(index_1_move == 0):
                value = partial_hand[x]
                index_1_count = partial_hand.count(value)
                #print(value)
            # if three values are within the same type
            if (value // 9 == (value+2) // 9):

                if(index_2_move == 0):
                    index_2_count = partial_hand.count(value+1)
                    #print(value+1)
                if(index_3_move == 0):
                    index_3_count = partial_hand.count(value+2)
                    #print(value+2)

                # print(str(index_1_count) + "," + str(index_2_count) + "," + str(index_3_count))

                # if there are at least one instance of each value
                if (index_1_count >0 and index_2_count >0 and index_3_count>0):

                    # if the numbers of each value are the same
                    if(index_1_count == index_2_count == index_3_count):
                        
                        # loop index advance move sum * 3
                        x += ((index_1_count)*3 + index_1_move + index_2_move + index_3_move)
                        index_1_count = 0
                        index_2_count = 0
                        index_3_count = 0
                        continue
                    # if the first value is the smallest
                    if (index_1_count <= index_2_count and index_1_count <= index_3_count):
                        
                        
                        
                        # index_2 and index_3 -= index_1, index_2_move and 3_move += index_1
                        index_2_count -= index_1_count
                        index_3_count -= index_1_count
                        index_2_move += index_1_count
                        index_3_move += index_1_count


                        # loop index advance index_1_move + index_1_count
                        if(index_2_count == 0 ):
                            x += (index_1_move+index_1_count+index_2_move)
                            index_1_count = index_3_count
                            index_1_move = index_3_move

                            index_2_count = 0
                            index_2_move = 0
                            index_3_count = 0
                            index_3_move = 0

                            value += 2
                            continue
                        
                        elif(index_3_count == 0 ):

                            x += (index_1_move+index_1_count+index_2_move+index_2_count+index_3_move)

                            index_1_count = 0
                            index_1_move = 0
                            index_2_count = 0
                            index_2_move = 0
                            index_3_count = 0
                            index_3_move = 0
                            continue

                        else:
                            x += (index_1_move+index_1_count)
                            # index_1 = index_2, index_2 = index_3, index_3 = 0
                            index_1_count = index_2_count
                            index_1_move = index_2_move
                            index_2_count = index_3_count
                            index_2_move = index_3_move
                            index_3_count = 0
                            index_3_move = 0
                            value += 1
                            continue
                    
                    elif (index_2_count <= index_1_count and index_2_count <= index_3_count):

                        index_1_count -= index_2_count
                        index_3_count -= index_2_count
                        index_1_move += index_2_count
                        index_3_move += index_2_count
                        
                        remain.extend([value for i in range(index_1_count)])
                        if(index_3_count == 0):
                            x += (index_1_move + index_1_count + index_2_move + index_2_count + index_3_move)
                            index_1_count = 0
                            index_2_count = 0
                            index_3_count = 0
                            index_1_move = 0 
                            index_2_move = 0
                            index_3_move = 0
                            continue

                        else:
                            x += (index_1_move + index_1_count + index_2_count + index_2_move)
                            index_1_count = index_3_count
                            index_1_move = index_3_move
                            index_2_count = 0
                            index_2_move = 0
                            index_3_count = 0
                            index_3_move = 0
                            value += 2
                            continue
                        
                        
                        
                    elif (index_3_count <= index_1_count and index_3_count <= index_2_count):
                        

                        # remaining 
                        index_1_count -= index_3_count
                        index_2_count -= index_3_count

                        index_1_move += index_3_count
                        index_2_move += index_3_count

                        remain.extend([value for i in range(index_1_count)])
                        remain.extend([(value+1) for i in range(index_2_count)])
                        # move index by the tile 
                        x += (index_1_move+ index_1_count + index_2_move + index_2_count + index_3_count + index_3_move)
                        
                        # adjust values
                        index_1_count = 0
                        index_2_count = 0
                        index_3_count = 0
                        index_1_move = 0
                        index_2_move = 0
                        index_3_move = 0 
                        continue
                                  


            x += (index_1_move + index_2_move + index_3_move + 1)
            remain.append(value)
            #print("# of index 1 added to remain "+ str(index_1_count))
            index_1_count = 0
            index_1_move = 0
            index_2_count = 0
            index_2_move = 0
            index_3_count = 0
            index_3_move = 0 

        # seq_extract v1.0
        # remain = []
        # remain.extend(hand[0:index])
        # duplicate = []
        # x = index
        # while x < (len(hand)-2):
        #     if(hand[x]//9 == hand[x+2]//9):
        #         while(hand[x] == hand[x+1] or hand[x+1] == hand[x+2]):
        #             if(hand[x] == hand[x+1]):
        #                 hand.count

        #         if(hand[x]+2 == hand[x+1]+1 == hand[x+2]):
        #             x+=3
        #             continue
                    
                    
        #     remain.append(hand[x])
        #     x+=1   

        if(x<len(partial_hand)-1):
            remain.append(partial_hand[x])
            remain.append(partial_hand[x+1])
            #print("append: " + str(partial_hand[x]))
        # print("extract seq:")
        # print(remain)
        return remain




    def single_handParti(self,attr):
        current_list = self.hands[attr]

        for x in range(len(current_list)):

            self.efficiency_map.setdefault(str(attr*9+x),0)
            if(current_list[x] == 4):
                    #1 KAN or 1 triplet + possible sequence
                self.partition.setdefault("KAN-triplet",[])
                self.partition["KAN-triplet"].append(attr*9+x)

            if(current_list[x] == 3):
                    # 1 triplet or 1 pair + possible sequence
                self.partition.setdefault("triplet",[])
                self.partition["triplet"].append(attr*9+x)
            if(current_list[x] == 2):
                    # 1 pair
                self.partition.setdefault("pair",[])
                self.partition["pair"].append(attr*9+x)

            if(x == 7 and current_list[x] >= 1):
                if(current_list[x-1] == 0 and current_list[x+1]>=1):
                    self.partition.setdefault("sequence_one-way",[])
                    self.partition["sequence_one-way"].append(attr*9+x-1)
                
            if(x < len(current_list)-2 and current_list[x] >= 1):
                if(current_list[x+1]==0 and current_list[x+2]):
                        # sequence middle
                    self.partition.setdefault("sequence_middle",[])
                    self.partition["sequence_middle"].append(attr*9+x)
                if(current_list[x+1]>=1 and current_list[x+2]==0):
                        #sequence two-way
                    if(x==0):
                        self.partition.setdefault("sequence_one-way",[])
                        self.partition["sequence_one-way"].append(attr*9+x)
                    else:
                        self.partition.setdefault("sequence_two-way",[])
                        self.partition["sequence_two-way"].append(attr*9+x) 
                if(current_list[x+1]>=1 and current_list[x+2]>=1):
                        #sequence complete
                    self.partition.setdefault("sequence_complete",[])
                    self.partition["sequence_complete"].append(attr*9+x)

                else:
                    self.partition.setdefault("single",[])
                    self.partition["single"].append(attr*9+x)
            elif(current_list[x] == 1):
                self.partition.setdefault("single",[])
                self.partition["single"].append(attr*9+x)
        

    # print tiles that are used in all the possible partitions
    def used_tile(self):
        used_tile_list = {}
        self.efficiency_map = defaultdict(int)
        for key in self.partition:
            for index in self.partition[key]:
                if("middle" in key): 
                    self.efficiency_map[index] +=1
                    self.efficiency_map[index+2] +=1
                elif("two-way" in key):
                    self.efficiency_map[index] +=1
                    self.efficiency_map[index+1] +=1
                else:
                    self.efficiency_map[index] +=1
        print(self.efficiency_map)
        return used_tile_list

    # print tiles that are needed for incomplete sequences 
    def tile_needed(self,input):
        waiting_tile_list = []
        for index in self.partition[input]:
            if("pair" in input or "single" in input):
                # get remaining tile at certain location
                # modify efficiency map value based on remaining tile
                value = self.remaining_tile(index) * 0.1
                self.efficiency_map[str(index)] += value


                waiting_tile_list.append(index)
            if("middle" in input):
                waiting_tile_list.append(index+1)
            if("two-way" in input):
                # can add a condition check to eliminate negative index
                waiting_tile_list.append(index-1)
                waiting_tile_list.append(index+2)
            if("one-way" in input):
                if(index%9==0):
                    waiting_tile_list.append(index+2)
                else:
                    waiting_tile_list.append(index)
        waiting_tile_list.sort()
        return waiting_tile_list

    def tile_use_count(self):
        for t in self.partition:
            for index in self.partition[t]:
                if("two-way" in t):
                    self.efficiency_map[str(index-1)] += 1
                    self.efficiency_map[str(index)] += 1
                    self.efficiency_map[str(index+1)] += 1
                elif("sequence" in t):
                    self.efficiency_map[str(index)] += 1
                    self.efficiency_map[str(index+1)] += 1
                    self.efficiency_map[str(index+2)] += 1
                else:
                    self.efficiency_map[str(index)] += 1
 


    def tile_efficiency(self): 
        # get the lowest value(s) from the efficiency map
        # if multiple 
        return None

    

dummy = MahjongAgent()
hand = [0,0,1,1,2,2,4,4,7,7,9,9,20,30]
hand_2 = [0,1,2,3,4,5,6,7,8,9,10,11,12,13]
hand_3 = [2,3,4,6,7,8,13,14,15,16,16,19,20,23]
hand_4 = [9,10,12,13,14,19,20,21,23,24,25,30,30,31]
hand_5 = [1,2,3,4,4,4,5,6,7,7,7,9,10,12]
hand_6 = [2,2,3,3,3,4,4,4,5,11,12]
hand_7 = [2, 2, 3, 4, 5, 5, 12, 13, 13, 14, 14, 15, 22, 23]
hand_test = [6,7,8,9,10,11,12,13]
#2, 11, 12, 13, 20, 21, 22, 28, 28, 29, 29
# imp 2, 2, 3, 4, 5, 5, 12, 13, 13, 14, 14, 15, 22, 23
# 1, 2, 2, 3, 12, 12, 19, 20, 21, 22, 23, 23, 24, 25
# 2, 3, 4, 12, 12, 14, 15, 16, 31, 31, 31
# 2, 2, 2, 4, 5, 6, 13, 14, 15, 16, 16, 21, 22, 23
# 3,3,4,4,5,5,5,6,6

# print(dummy.tenpai_status_check(hand_6))



# dummy = MahjongAgent()
# dummy.single_handParti(0)
# dummy.single_handParti(1)
# dummy.single_handParti(2)
# dummy.tile_use_count()
# print(len(dummy.partition))
# print(dummy.partition)
# print(dummy.tile_needed())
# print(dummy.efficiency_map)

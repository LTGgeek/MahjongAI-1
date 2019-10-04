import csv
import random

import MahjongKit as mjkit
import MahjongAgent as mjagent

from os import path
from os import remove

def main():
    random.seed()
    glc = mjkit.GameLogCrawler()
    agent = mjagent.MahjongAgent()
    gene = glc.db_get_logs_where_players_lv_gr(19)
    # glc.db_show_tables()
    Errors = {}
    with open('test.csv', 'a') as csvFile:
        wr = csv.writer(csvFile, lineterminator='\n')
    if not path.exists('test.csv'):     
        # remove('test.csv')
        header = []
        for i in range(9):
            header.append('Discard_{}'.format(i))
        header.append('hand')
        header.append('random_tile')
        header.append('waiting_tile')
        header.append('result')
        wr.writerow(header)
    for i in range(100):
        try:
            log = gene.__next__()
            res = mjkit.PreProcessing.process_one_log(log)
            for r, sa in res.items():
                for state in sa[-1:]:
                    if(len(state.s_discard34) < 9):
                        continue
                    random_tile = random.randrange(34)
                    testhand = state.s_hand34
                    testhand.append(random_tile)
                    testhand.sort()
                    discard = state.s_discard34[:9]
                    row = []
                    row.extend(discard)
                    row.append(state.s_hand34)
                    row.append(random_tile)
                    # print('discard and hand:', row)
                    waiting_tile = []
                    waiting_dict = agent.tenpai_status_check(testhand)
                    # print('waiting_dict:', waiting_dict)
                    for dis in waiting_dict:
                        if(type(waiting_dict[dis]) is int):
                            waiting_tile.append(waiting_dict[dis])
                        else: waiting_tile.extend(waiting_dict[dis])
                        if random_tile in waiting_tile:
                            result = 1
                        else: result = 0
                        
                    row.append(waiting_tile)
                    row.append(result)
                    # print('final:', row)
                    # wr = csv.writer(csvFile)
                    wr.writerow(row)
            print("Finished writing log {}".format(i))
        except Exception as e:
            # print(e)
            pass
    # print('Finished Writing to CSV')



if __name__ == '__main__':
    main()
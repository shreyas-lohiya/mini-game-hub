import matplotlib.pyplot as plt
import csv

def main():
    totwins={}
    gameplayfreq={'tictactoe':0, 'othello':0, 'connect4':0}
    with open('history.csv') as f:
        for field in csv.reader(f):
            if field[0] in totwins:
                totwins[field[0]]+=1
            else:
                totwins[field[0]]=1
            if field[1] not in totwins:
                totwins[field[1]]=0
            gameplayfreq[field[3]]+=1
    sortedtotwins = sorted(totwins.items(), key=lambda x: x[1], reverse=True)
    top5=[]
    for item in sortedtotwins:
        if len(top5)<5:
            top5.append(item)
        elif item[1]==top5[4][1]:
            top5.append(item)
        else:
            break
    fontforplottitle = {'family':'serif','color':'blue','size':20}
    plt.subplot(2,2,1)
    plt.bar([x[0] for x in top5],[x[1] for x in top5])
    plt.title("Top 5 Players",fontdict=fontforplottitle)
    plt.ylabel("Total number of wins")
    plt.subplot(2,2,2)
    plt.pie(list(totwins.values()),labels=list(totwins.keys()))
    plt.title("Total number of wins",fontdict=fontforplottitle)
    plt.subplot(2,1,2)
    plt.pie(list(gameplayfreq.values()),labels=list(gameplayfreq.keys()))
    plt.title("Most Played Games",fontdict=fontforplottitle)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main() 
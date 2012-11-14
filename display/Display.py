class Display():

    def emptyMatrix(self,y,x):
        frame = []
        for i in range(y):
            frame.append([])
        for i in range(y):
            for j in range(x):
                frame[i].append(0)
        return frame

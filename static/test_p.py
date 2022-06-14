def minimumTotal(triangle):
    """
    :type triangle: List[List[int]]
    :rtype: int
    """
    mins,x =triangle[0][0] , 1
    if len(triangle) > 1:
        while x < len(triangle):

            y = min(triangle[x])
            #print(y)
            mins = mins + y
            x=x+1 

        return mins 
    else:
        return mins


print(minimumTotal([[-1],[2,3],[1,-1,-3]]))
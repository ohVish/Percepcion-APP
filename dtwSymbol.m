function type = dtwSymbol(vector)
    minDist = Inf;
    
    load('clavesSol.mat');
    for i=1:size(clavesSol,1)
        dist = dtw(vector,clavesSol(i,:));
        if dist < minDist
            type = '0';
            minDist = dist;
        end
    end
    
    load('negras.mat');
    for i=1:size(negras,1)
        dist = dtw(vector,negras(i,:));
        if dist < minDist
            type = '4';
            minDist = dist;
        end
    end
    
    load('corcheasDown.mat');
    for i=1:size(corcheasDown,1)
        dist = dtw(vector,corcheasDown(i,:));
        if dist < minDist
            type = '8';
            minDist = dist;
        end
    end
    
    load('corcheasUp.mat');
    for i=1:size(corcheasUp,1)
        dist = dtw(vector,corcheasUp(i,:));
        if dist < minDist
            type = '8';
            minDist = dist;
        end
    end
end


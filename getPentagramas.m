im = imread(filename);
close all;
gray=rgb2gray(im);
bw=imbinarize(gray, umbral);
bw=logical(1-bw);
imshow(bw,[]);

N = 1;
[rows, columns, numColorChannels] = size(bw);
numOutputRows = round(rows/N);
numOutputColumns = round(columns/N);
bw = imresize(bw, [numOutputRows, numOutputColumns]);

etiquetas = bwconncomp(bw,8);
tam=cellfun('size',etiquetas.PixelIdxList,1);
coeficiente = max(tam)*0.5;
pentagramasEtiquetas = find(tam > coeficiente);

pentagramas = cell(length(pentagramasEtiquetas),2);

for i=1:length(pentagramasEtiquetas)
    aux = zeros(size(bw));
    aux(etiquetas.PixelIdxList{pentagramasEtiquetas(i)}) = 1;
    
    [fila, columna] = find(aux == 1);
    pentImg = aux(min(fila)-20:max(fila)+20,:);
    pentagramas{i,1} = getNotas2(pentImg,valorLineas);
    pentagramas{i,2} = min(fila);
end

pentagramas = sortrows(pentagramas,2);

%pentagramas = pentagramas{:,1};
%Imprimir datos
str=[];
for i = 1:length(pentagramas)
    aux=pentagramas{i,1};
    for j = 1:length(aux)
        if ~isempty(aux{j}) && ~strcmp(aux{j}.Simbolo, '0')
            str = [str,' ',aux{j}.Tono,aux{j}.Simbolo];
        end
    end
end
 
save('pentagramas','pentagramas');
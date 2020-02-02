%% Cargar datos
pentagramas=load ('pentagramas.mat');

pentagrama1=pentagramas.pentagramas{1};

%% Usando transformada de hough circular
[H, theta, rho] = hough(pentagrama1);
peaks =  houghpeaks(H,1,"Threshold",50);
lines = houghlines(pentagrama1, theta, rho, peaks,'FillGap',10);

pentagrama1 = imrotate(pentagrama1,-(90 - abs(lines.theta)));

[fila, columna] = find(pentagrama1 == 1);
    
pentagrama1 = pentagrama1(min(fila)-5:max(fila)+5,:);

[centers, radii, metric] = imfindcircles(pentagrama1,[1 200],'ObjectPolarity','bright');

pos=find(radii <= 3 | radii >= 6);

centers(pos,:)=[];
radii(pos)=[];
metric(pos)=[];

%figure;
%hold on;
%subplot(1,2,1);
%imshow(pentagrama1,[]);

%viscircles(centers,radii,'EdgeColor','b'); hold off;

v=sum(pentagrama1, 2);
verticalProfile = v-mean(v); 

%subplot(1,2,2);
%barh(flip(verticalProfile));
    

%Obtengo los valores de las lineas del pentagrama
lineas=find(ismember(verticalProfile, maxk(verticalProfile,5)));

%Añado 3 lineas por encima y 3 por debajo
dis=lineas(2)-lineas(1);
    
lineas=[lineas(1)-dis;lineas;lineas(end)+dis];

%figure;
[~,posOrdenadas]=sort(centers(:,1));
notas=cell(length(posOrdenadas),1);
j=1;
for i=(1:length(posOrdenadas))
    rad=radii(posOrdenadas(i));
    centx=centers(posOrdenadas(i),1);
    centy=centers(posOrdenadas(i),2);
    
    simbolo=pentagrama1(:,round(centx-rad*1.6):round(centx+rad*1.6));
    
    corta=[];
    
    for l=(1:length(lineas))
        [x,y]=linecirc(0,lineas(l),centx,centy,rad);
        
        if ~isnan(sum(x))
            corta=[corta,l];
        end
    end
    
    if ~isempty(corta)
        media =mean(corta);
        centro = centx;
        j=j+1;
    end
    
    
    nota = struct('Tono',media,'Posicion',centro,'Simbolo',simbolo);
    
    notas{j} = nota;
    %subplot(2,ceil(length(centers)/2),i);
    %imshow(simbolo,[]);    
end


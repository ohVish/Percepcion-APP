function notas = getNotas2(pentagrama,valorLineas)
    load('tonos.mat')
    [H, theta, rho] = hough(pentagrama);
    peaks =  houghpeaks(H,1);

    lines = houghlines(pentagrama, theta, rho, peaks);

    pentagrama = imrotate(pentagrama,-(90 - abs(lines(1).theta)));

    [fila, ~] = find(pentagrama == 1);

    pentagrama = pentagrama(min(fila)-5:max(fila)+5,:);
    
    %Obtengo los valores de las lineas del pentagrama
    v=sum(pentagrama, 2);
    verticalProfile = v-mean(v); 
    [picos,locs] =  findpeaks(verticalProfile,'MinPeakDistance',valorLineas);
    
    figure;
    subplot(1,2,1);
    imshow(pentagrama,[]);
    subplot(1,2,2);
    barh(verticalProfile);
    
    valores = maxk(picos,5);
    %disp(valores);
    lineas=ones(5,1);
    for cont = (1:5)
        lineas(cont) = locs(find(picos == valores(cont),1,'first'));
        picos(find(picos == valores(cont),1,'first')) = 0;
    end

    
    lineas = sort(lineas);
    
    rad = (lineas(2) - lineas(1))/2 * 1.5;
    
    lineas = [lineas(1)-(lineas(2) - lineas(1)); lineas; lineas(end)+(lineas(2) - lineas(1))];
    
    struture = strel('rectangle',[8 1]);
    E = imerode(pentagrama,struture);
    E = imdilate(E,struture);

    figure; imshow(E);

    simbolos = bwconncomp(E,8);

    tam=cellfun('size',simbolos.PixelIdxList,1);
    coeficiente = mean(tam)*0.5;
    simbolosEtiquetas = find(tam > coeficiente);    
    
    figure;
    notas=cell(length(simbolosEtiquetas),1);

    j=1;
    for i = (1:length(simbolosEtiquetas))
        aux = zeros(size(E));
        aux(simbolos.PixelIdxList{simbolosEtiquetas(i)}) = 1;

        [~, columna] = find(aux == 1);
        if min(columna)-5 > 1
            tamIni = min(columna)-5;
        else
            tamIni = min(columna);
        end
        
        if max(columna)+5 < size(aux,2)
            tamFin = max(columna)+5;
        else
            tamFin = max(columna);
        end
        
        prueba = E(:,tamIni:tamFin);

        struture = strel('rectangle',[1 15]);
        H = imerode(prueba,struture);
        H = imdilate(H,struture);
        
        CC = bwconncomp(H);
        centro = regionprops(CC,'centroid');
        
        if size(centro) >= 1
            x = centro(1).Centroid(1);
            y = centro(1).Centroid(2);

            corta=[];

            for k=(1:length(lineas))
                [cortex,~]=linecirc(0,lineas(k),x,y,rad);

                if ~isnan(sum(cortex))
                    corta=[corta,k];

                end
            end

            % MOSTRAR CIRCULOS Y LINEAS DEL PENTAGRAMA
            subplot(2,ceil(length(simbolosEtiquetas)/2),i);
            imshow(prueba);
            hold on;
            plot(lineas);
            viscircles([x,y],rad,'EdgeColor','b');
            values=1:size(H,2);
            plot(values,lineas*ones(size(values)))
            hold off;


            if ~isempty(corta)
                simbolo=dtwSymbol(invmoments(prueba));
                %simbolo=invmoments(prueba);
                media = tonos(mean(corta));

                nota = struct('Tono',media,'Simbolo',simbolo);
                notas{j} = nota;

                j=j+1;
            end
        end
    end
end


y = audioread(filename);

% Fs = 8000
% N = Fs * duracion(s)
% N = length(y);
inicio = find(y > 0.1);
y = y(inicio(1):end);

% Tempo: Negra = 60 => Negra = 8000 muestras
% Semicorchea = 2000 muestras
TEMPO = 60;
SEGMENTOS = buffer(y, round(2000 * 60/TEMPO));
NOTAS = zeros(length(SEGMENTOS(1,:))-1, 1); 
OCTAVAS = NOTAS;

load FRECUENCIAS;
for i = 1:length(SEGMENTOS(1,:))-1
   NOTAS(i) = mean(pitch(SEGMENTOS(:,i),8000));
   [NOTAS(i), OCTAVAS(i)] = aproximar(NOTAS(i), FRECUENCIAS);
end
clear FRECUENCIAS;

load notas_str;
duracion = 1;
str = '';

for i = 2:length(NOTAS)
    
    % Duracion
    if (NOTAS(i) == NOTAS(i-1) && i < length(NOTAS))
        duracion = duracion + 1;
    else
        
        while duracion > 0
           % Nota
            str = strcat(str,notas_str(NOTAS(i-1)));
    
            %Octava
            for j = 1:OCTAVAS(i-1)-1
               str = strcat(str,"'"); 
            end
                       
            if duracion > 16
                str = strcat(str,"1 ");
                duracion = duracion - 16;
            elseif duracion > 8
                str = strcat(str,"2 ");
                duracion = duracion - 8;
            elseif duracion > 4
                str = strcat(str,"4 ");
                duracion = duracion - 4;
            elseif duracion > 2
                str = strcat(str,"8 ");
                duracion = duracion - 2;
            else
                str = strcat(str,"16 ");
                duracion = 0;
            end    
        end
        
       duracion = 1;
       
    end
end
str = convertStringsToChars(str);

clear notas_str










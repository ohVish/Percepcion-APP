function [nota, octava] = aproximar(F, FRECUENCIAS)
    menor = find(FRECUENCIAS <= F);
    menor = FRECUENCIAS(menor(end));

    mayor = find(FRECUENCIAS >= F);
    mayor = FRECUENCIAS(mayor(1));
    
    DIF = mayor - F;
    dif = F - menor;
    
    if DIF > dif
        F = menor;
    else
        F = mayor;
    end
    
    [nota,octava] = find(FRECUENCIAS == F);

end
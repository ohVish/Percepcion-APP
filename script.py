import matlab.engine

sesion = matlab.engine.start_matlab()

sesion.getPentagramas(nargout=0)

a = sesion.workspace['str']


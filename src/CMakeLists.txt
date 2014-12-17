include_directories(
    ${CMAKE_CURRENT_SOURCE_DIR}
    )

cython_add_module(scintillator scintillator.py)
cython_add_module(pmt pmt.py)
cython_add_module(cable cable.py)
cython_add_module(digitize digitize.py)

configure_file(dacsim.py ${CMAKE_BINARY_DIR}/dacsim.py)
execute_process(COMMAND chmod 755 ${CMAKE_BINARY_DIR}/dacsim.py)
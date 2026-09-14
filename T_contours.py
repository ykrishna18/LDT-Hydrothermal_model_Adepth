import pyvista as pv

mesh = pv.read("VTK/test_fault_10m_269.vtk")

# Convert T to point data
if "T" in mesh.cell_data:
    mesh = mesh.cell_data_to_point_data()

mesh["T_C"] = mesh["T"] - 273.15

print("Temperature range:",
      mesh["T_C"].min(),
      mesh["T_C"].max())

levels = [50, 100, 200, 300, 400, 500, 600, 700]

# Extract the actual 2D surface
surf = mesh.extract_surface()

contours = surf.contour(
    isosurfaces=levels,
    scalars="T_C"
)

print("Contour points:", contours.n_points)
print("Contour cells:", contours.n_cells)

p = pv.Plotter()

p.enable_anti_aliasing()

p.add_mesh(
    surf,
    scalars="T_C",
    cmap="turbo",
    show_edges=False
)

p.add_mesh(
    contours,
    color="black",
    line_width=10,
    render_lines_as_tubes=True
)

p.add_scalar_bar(
    title="Temperature (°C)"
)



p.set_background("white")

contours.save("temperature_contours_3.vtp")

p.view_xy()
p.show()

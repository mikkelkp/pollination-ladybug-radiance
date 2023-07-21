if __name__ == '__main__':
    import pathlib
    import json

    from ladybug_radiance.study.directsun import DirectSunStudy
    from ladybug_geometry.geometry3d import Vector3D, Mesh3D

    vectors_file = pathlib.Path('sun_vectors.txt')
    context_file = pathlib.Path('context_geo.json')
    geometry_file = pathlib.Path('input_geo.json')

    with vectors_file.open('r') as inf:
        vectors = [
            Vector3D(*(float(v) for v in line.split(',')))
            for line in inf
        ]

    input_geo = json.loads(geometry_file.read_text())
    study_mesh = Mesh3D.from_dict(input_geo)

    context_geo = []
    if context_file.is_file():
        context_data = json.loads(context_file.read_text())
        context_geo = [Mesh3D.from_dict(context_data)]

    timestep = {{self.timestep}}
    offset_distance = {{self.offset_dist}}

    study = DirectSunStudy(
        vectors=vectors, study_mesh=study_mesh, context_geometry=context_geo,
        timestep=timestep, offset_distance=offset_distance
    )

    study.compute()
    colored_mesh, *_ = study.draw()

    output_folder = pathlib.Path('results')
    output_folder.mkdir(parents=True, exist_ok=True)

    output_file = output_folder.joinpath('results.json')
    output_file.write_text(json.dumps(study.direct_sun_hours))

    vsf_file = output_folder.joinpath('output.vsf')
    vsf_file.write_text(json.dumps(colored_mesh.to_dict()))

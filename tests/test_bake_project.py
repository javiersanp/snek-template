def test_basic_bake_ok(cookies):
    result = cookies.bake(extra_context={'project_name': 'Foo Bar-Taz'})
    assert result.exit_code == 0, "Template render without errors"
    assert result.project.basename == 'foo_bar_taz', "Test project slug"

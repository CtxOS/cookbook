from pathlib import Path

import click

from ctxcook.config import get_environment_config
from ctxcook.exporter import export_notebook
from ctxcook.generator import TemplateGenerator
from ctxcook.notebook import build_notebook
from ctxcook.parser import load_recipe
from ctxcook.requirements import RequirementsGenerator
from ctxcook.validator import validate


@click.group()
def main():
    """CtxOS AI Cookbook Engine - Convert Declarative AI Recipes → Executable Infrastructure"""
    pass


@main.command()
@click.argument("recipe_path")
@click.option("--output", default="output.ipynb", help="Output notebook path")
@click.option(
    "--environment",
    default="colab",
    type=click.Choice(["colab", "docker", "local"]),
    help="Target environment for notebook generation",
)
@click.option("--requirements", help="Generate requirements.txt file")
@click.option("--dockerfile", help="Generate Dockerfile")
@click.option("--hf-deploy", help="Generate Hugging Face deployment config")
def build(recipe_path, output, environment, requirements, dockerfile, hf_deploy):
    """Build a notebook from a YAML recipe with enhanced options"""
    try:
        recipe = load_recipe(recipe_path)
        validate(recipe)

        # Generate notebook with environment-specific templating
        nb = build_notebook(recipe, environment)
        export_notebook(nb, output)
        click.echo(f"✅ Notebook generated: {output}")

        # Generate additional files if requested
        generator = TemplateGenerator()
        req_gen = RequirementsGenerator()

        if requirements:
            req_content = req_gen.generate_requirements(recipe, environment)
            Path(requirements).write_text(req_content)
            click.echo(f"✅ Requirements file generated: {requirements}")

        if dockerfile:
            docker_content = generator.render_dockerfile(recipe)
            Path(dockerfile).write_text(docker_content)
            click.echo(f"✅ Dockerfile generated: {dockerfile}")

        if hf_deploy:
            hf_content = generator.render_hf_deploy(recipe)
            Path(hf_deploy).write_text(hf_content)
            click.echo(f"✅ Hugging Face deployment config generated: {hf_deploy}")

        # Show environment info
        env_config = get_environment_config(environment)
        click.echo(f"\n🚀 Environment: {environment.title()}")
        click.echo(f"   GPU Support: {env_config.gpu_support}")
        click.echo(f"   Memory Optimized: {env_config.memory_optimized}")
        click.echo(f"   Python Version: {env_config.python_version}")

    except Exception as e:
        click.echo(f"❌ Error: {e}", err=True)
        raise click.Abort()


@main.command()
@click.argument("recipe_path")
@click.option(
    "--environment", default="colab", type=click.Choice(["colab", "docker", "local"])
)
def info(recipe_path, environment):
    """Show recipe information and environment configuration"""
    try:
        recipe = load_recipe(recipe_path)
        validate(recipe)

        click.echo(f"📋 Recipe: {recipe['name']}")
        click.echo(f"   Model: {recipe['model']['base']}")
        click.echo(
            f"   Dataset: {recipe['dataset'].get('name', recipe['dataset'].get('source', 'local'))}"
        )
        if recipe["model"].get("quantization"):
            click.echo(f"   Quantization: {recipe['model']['quantization']}")

        click.echo(f"\n🔧 Environment: {environment.title()}")
        env_config = get_environment_config(environment)
        click.echo(f"   Python: {env_config.python_version}")
        click.echo(f"   GPU Support: {env_config.gpu_support}")
        click.echo(f"   Auto Install: {env_config.auto_install}")
        click.echo(f"   Special Features: {', '.join(env_config.special_features)}")

    except Exception as e:
        click.echo(f"❌ Error: {e}", err=True)
        raise click.Abort()


@main.command()
def versions():
    """Show dependency version information"""
    req_gen = RequirementsGenerator()
    versions = req_gen.get_version_info()
    
    click.echo("📦 Dependency Versions:")
    for package, version in versions.items():
        click.echo(f"   {package}: {version}")


if __name__ == "__main__":
    main()

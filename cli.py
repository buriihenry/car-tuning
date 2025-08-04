#!/usr/bin/env python3
"""
Command Line Interface for the Car Tuning AI Agent.
Provides an interactive way to generate car tuning recommendations.
"""

import typer
import json
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich.progress import Progress, SpinnerColumn, TextColumn
from typing import Optional, List

from src.main import CarTuningAgent
from src.models import CarInfo, UserPreferences, EngineType, DrivingGoal, BudgetRange, ExperienceLevel

app = typer.Typer(help="Car Tuning AI Agent - Get personalized car modification recommendations")
console = Console()


def print_banner():
    """Print application banner."""
    banner = """
    ╔══════════════════════════════════════════════════════════════╗
    ║                    CAR TUNING AI AGENT                      ║
    ║                                                              ║
    ║  Get personalized car modification recommendations based on  ║
    ║  your vehicle, goals, budget, and experience level.        ║
    ╚══════════════════════════════════════════════════════════════╝
    """
    console.print(Panel(banner, style="bold blue"))


def get_car_info() -> CarInfo:
    """Interactive car information collection."""
    console.print("\n[bold cyan]📋 CAR INFORMATION[/bold cyan]")
    console.print("Let's start by gathering information about your vehicle.\n")
    
    # Car make
    make = typer.prompt("Car make (e.g., Toyota, BMW, Tesla)", type=str)
    
    # Car model
    model = typer.prompt("Car model (e.g., Camry, 3 Series, Model 3)", type=str)
    
    # Year
    year = typer.prompt("Manufacturing year", type=int)
    
    # Engine type
    engine_types = [et.value for et in EngineType]
    console.print(f"\nAvailable engine types: {', '.join(engine_types)}")
    engine_type_str = typer.prompt(
        "Engine type",
        type=str,
        default="petrol"
    )
    
    # Validate engine type
    if engine_type_str not in engine_types:
        console.print(f"[red]Invalid engine type. Using 'petrol' as default.[/red]")
        engine_type_str = "petrol"
    
    engine_type = EngineType(engine_type_str)
    
    # Current modifications
    console.print("\n[yellow]Current modifications (optional):[/yellow]")
    console.print("Enter your current modifications, one per line. Press Enter twice when done.")
    
    modifications = []
    while True:
        mod = input("Modification (or Enter to finish): ").strip()
        if not mod:
            break
        modifications.append(mod)
    
    return CarInfo(
        make=make,
        model=model,
        year=year,
        engine_type=engine_type,
        current_modifications=modifications
    )


def get_user_preferences() -> UserPreferences:
    """Interactive user preferences collection."""
    console.print("\n[bold cyan]🎯 DRIVING GOALS[/bold cyan]")
    console.print("What are your primary goals for car modifications?\n")
    
    goals = []
    goal_options = [goal.value for goal in DrivingGoal]
    
    for i, goal in enumerate(goal_options, 1):
        console.print(f"{i}. {goal.replace('_', ' ').title()}")
    
    console.print("\nSelect your goals (comma-separated numbers, e.g., 1,3):")
    goal_indices = typer.prompt("Goals", type=str)
    
    try:
        indices = [int(x.strip()) - 1 for x in goal_indices.split(",")]
        goals = [DrivingGoal(goal_options[i]) for i in indices if 0 <= i < len(goal_options)]
    except (ValueError, IndexError):
        console.print("[red]Invalid selection. Using performance as default.[/red]")
        goals = [DrivingGoal.PERFORMANCE]
    
    console.print("\n[bold cyan]💰 BUDGET[/bold cyan]")
    budget_options = [br.value for br in BudgetRange]
    console.print(f"Available budget ranges: {', '.join(budget_options)}")
    budget_str = typer.prompt(
        "Budget range",
        type=str,
        default="moderate"
    )
    
    # Validate budget range
    if budget_str not in budget_options:
        console.print(f"[red]Invalid budget range. Using 'moderate' as default.[/red]")
        budget_str = "moderate"
    
    budget_range = BudgetRange(budget_str)
    
    # Optional specific budget
    max_budget = None
    if typer.confirm("Do you have a specific maximum budget?"):
        max_budget = typer.prompt("Maximum budget (USD)", type=float)
    
    console.print("\n[bold cyan]👤 EXPERIENCE LEVEL[/bold cyan]")
    experience_options = [el.value for el in ExperienceLevel]
    console.print(f"Available experience levels: {', '.join(experience_options)}")
    experience_str = typer.prompt(
        "Experience level",
        type=str,
        default="intermediate"
    )
    
    # Validate experience level
    if experience_str not in experience_options:
        console.print(f"[red]Invalid experience level. Using 'intermediate' as default.[/red]")
        experience_str = "intermediate"
    
    experience_level = ExperienceLevel(experience_str)
    
    return UserPreferences(
        primary_goals=goals,
        budget_range=budget_range,
        experience_level=experience_level,
        max_budget=max_budget
    )


def display_recommendations(report):
    """Display tuning recommendations in a formatted way."""
    console.print("\n" + "="*80)
    console.print("[bold green]🎯 TUNING RECOMMENDATIONS[/bold green]")
    console.print("="*80)
    
    # Car and user info summary
    car_info = report.car_info
    user_prefs = report.user_preferences
    
    summary_table = Table(title="Vehicle & Preferences Summary")
    summary_table.add_column("Category", style="cyan")
    summary_table.add_column("Details", style="white")
    
    summary_table.add_row("Vehicle", f"{car_info.year} {car_info.make} {car_info.model}")
    summary_table.add_row("Engine", car_info.engine_type.value.title())
    summary_table.add_row("Goals", ", ".join([g.value.replace("_", " ").title() for g in user_prefs.primary_goals]))
    summary_table.add_row("Budget", f"{user_prefs.budget_range.value.title()} (${report.total_estimated_cost['min']:,.0f} - ${report.total_estimated_cost['max']:,.0f})")
    summary_table.add_row("Experience", user_prefs.experience_level.value.title())
    
    console.print(summary_table)
    
    # Recommendations
    console.print(f"\n[bold]📋 RECOMMENDATIONS ({len(report.recommendations)})[/bold]")
    
    for i, rec in enumerate(report.recommendations, 1):
        console.print(f"\n[bold cyan]{i}. {rec.name}[/bold cyan]")
        console.print(f"   Category: {rec.category.value.replace('_', ' ').title()}")
        console.print(f"   Description: {rec.description}")
        console.print(f"   Cost: ${rec.cost_range['min']:,.0f} - ${rec.cost_range['max']:,.0f}")
        console.print(f"   Priority Score: {rec.priority_score:.1f}/10")
        console.print(f"   Safety Level: {rec.safety_level.value.title()}")
        console.print(f"   Installation: {rec.installation_difficulty}")
        
        if rec.benefits:
            console.print("   [green]Benefits:[/green]")
            for benefit in rec.benefits:
                console.print(f"     • {benefit}")
        
        if rec.safety_warnings:
            console.print("   [red]Safety Warnings:[/red]")
            for warning in rec.safety_warnings:
                console.print(f"     ⚠️  {warning}")
        
        if rec.legal_considerations:
            console.print("   [yellow]Legal Considerations:[/yellow]")
            for legal in rec.legal_considerations:
                console.print(f"     ⚖️  {legal}")
    
    # Safety and Legal Summary
    if report.safety_summary["high_risk"]:
        console.print("\n[bold red]🚨 HIGH RISK WARNINGS[/bold red]")
        for warning in report.safety_summary["high_risk"]:
            console.print(f"   ⚠️  {warning}")
    
    if report.legal_summary["warranty_impacts"]:
        console.print("\n[bold yellow]📋 WARRANTY IMPACTS[/bold yellow]")
        for impact in report.legal_summary["warranty_impacts"]:
            console.print(f"   📄 {impact}")
    
    # Disclaimer
    console.print(f"\n[bold red]DISCLAIMER[/bold red]")
    console.print(report.disclaimer)


@app.command()
def interactive():
    """Start interactive car tuning recommendation process."""
    print_banner()
    
    try:
        # Get car information
        car_info = get_car_info()
        
        # Get user preferences
        user_preferences = get_user_preferences()
        
        # Generate recommendations
        console.print("\n[bold]🤖 Generating recommendations...[/bold]")
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            task = progress.add_task("Analyzing vehicle and preferences...", total=None)
            
            agent = CarTuningAgent()
            report = agent.generate_recommendations(car_info, user_preferences)
        
        # Display results
        display_recommendations(report)
        
        # Export option
        if typer.confirm("\nWould you like to export the report to JSON?"):
            export_path = typer.prompt("Export file path", default="tuning_report.json")
            with open(export_path, 'w') as f:
                f.write(agent.export_report_as_json(report))
            console.print(f"[green]Report exported to {export_path}[/green]")
    
    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]")
        raise typer.Exit(1)


@app.command()
def from_file(
    input_file: Path = typer.Argument(..., help="JSON file with car info and preferences")
):
    """Generate recommendations from a JSON file."""
    print_banner()
    
    try:
        with open(input_file, 'r') as f:
            data = json.load(f)
        
        agent = CarTuningAgent()
        report = agent.generate_recommendations_from_dict(data)
        
        display_recommendations(report)
        
    except FileNotFoundError:
        console.print(f"[red]Error: File {input_file} not found[/red]")
        raise typer.Exit(1)
    except json.JSONDecodeError:
        console.print(f"[red]Error: Invalid JSON in {input_file}[/red]")
        raise typer.Exit(1)
    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]")
        raise typer.Exit(1)


@app.command()
def sample():
    """Generate a sample recommendation report."""
    print_banner()
    
    try:
        agent = CarTuningAgent()
        sample_data = agent.get_sample_request()
        
        console.print("[yellow]Using sample data:[/yellow]")
        console.print(json.dumps(sample_data, indent=2))
        console.print()
        
        report = agent.generate_recommendations_from_dict(sample_data)
        display_recommendations(report)
        
    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]")
        raise typer.Exit(1)


@app.command()
def options():
    """Show available options for the system."""
    print_banner()
    
    agent = CarTuningAgent()
    options = agent.get_available_options()
    
    console.print("[bold cyan]Available Options[/bold cyan]\n")
    
    # Engine types
    console.print("[bold]Engine Types:[/bold]")
    for et in options["engine_types"]:
        console.print(f"  • {et}")
    
    # Driving goals
    console.print("\n[bold]Driving Goals:[/bold]")
    for goal in options["driving_goals"]:
        console.print(f"  • {goal.replace('_', ' ').title()}")
    
    # Budget ranges
    console.print("\n[bold]Budget Ranges:[/bold]")
    for br in options["budget_ranges"]:
        console.print(f"  • {br.replace('_', ' ').title()}")
    
    # Experience levels
    console.print("\n[bold]Experience Levels:[/bold]")
    for el in options["experience_levels"]:
        console.print(f"  • {el.replace('_', ' ').title()}")
    
    # Car makes
    console.print(f"\n[bold]Supported Car Makes ({len(options['valid_makes'])}):[/bold]")
    for make in options["valid_makes"][:10]:  # Show first 10
        console.print(f"  • {make}")
    if len(options["valid_makes"]) > 10:
        console.print(f"  ... and {len(options['valid_makes']) - 10} more")


if __name__ == "__main__":
    app() 
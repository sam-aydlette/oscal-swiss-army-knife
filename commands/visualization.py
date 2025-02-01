from typing import Dict, Any
import json
from pathlib import Path
import matplotlib.pyplot as plt
import networkx as nx
from datetime import datetime

class OSCALVisualizer:
    """Class for creating visualizations of OSCAL data"""
    
    def __init__(self, output_dir: str = "reports"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
    def create_component_graph(self, oscal_file: Dict[str, Any]) -> str:
        """Create a graph visualization of system components"""
        G = nx.DiGraph()
        
        try:
            components = oscal_file["system-security-plan"]["system-implementation"]["components"]
            
            # Add nodes for each component
            for comp in components:
                G.add_node(comp["title"], type=comp["type"])
                
                # Add edges for relationships
                if "links" in comp:
                    for link in comp["links"]:
                        G.add_edge(comp["title"], link["text"])
                        
            # Generate the visualization
            plt.figure(figsize=(12, 8))
            pos = nx.spring_layout(G)
            nx.draw(G, pos, with_labels=True, node_color='lightblue', 
                   node_size=2000, font_size=8, font_weight='bold')
                   
            # Save the graph
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = self.output_dir / f"component_graph_{timestamp}.png"
            plt.savefig(output_path)
            plt.close()
            
            return str(output_path)
            
        except KeyError as e:
            raise ValueError(f"Unable to create component graph: {str(e)}")
            
    def generate_html_report(self, oscal_file: Dict[str, Any]) -> str:
        """Generate an HTML report of the OSCAL document"""
        try:
            # Basic template
            html_content = """
            <!DOCTYPE html>
            <html>
            <head>
                <title>OSCAL Report</title>
                <style>
                    body { font-family: Arial, sans-serif; margin: 40px; }
                    .section { margin-bottom: 20px; }
                    .metadata { background-color: #f5f5f5; padding: 10px; }
                    .component { border: 1px solid #ddd; padding: 10px; margin: 5px; }
                </style>
            </head>
            <body>
            """
            
            # Add metadata
            if "system-security-plan" in oscal_file:
                metadata = oscal_file["system-security-plan"].get("metadata", {})
                html_content += f"""
                <div class="section metadata">
                    <h2>Metadata</h2>
                    <p>Title: {metadata.get('title', 'N/A')}</p>
                    <p>Version: {metadata.get('version', 'N/A')}</p>
                    <p>Last Modified: {metadata.get('last-modified', 'N/A')}</p>
                </div>
                """
            
            # Add components if present
            if "system-implementation" in oscal_file.get("system-security-plan", {}):
                components = oscal_file["system-security-plan"]["system-implementation"].get("components", [])
                html_content += """
                <div class="section">
                    <h2>Components</h2>
                """
                for comp in components:
                    html_content += f"""
                    <div class="component">
                        <h3>{comp.get('title', 'Unnamed Component')}</h3>
                        <p>Type: {comp.get('type', 'N/A')}</p>
                        <p>Description: {comp.get('description', 'N/A')}</p>
                    </div>
                    """
                    
            html_content += """
            </body>
            </html>
            """
            
            # Save the report
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = self.output_dir / f"oscal_report_{timestamp}.html"
            output_path.write_text(html_content)
            
            return str(output_path)
            
        except Exception as e:
            raise ValueError(f"Unable to generate HTML report: {str(e)}")
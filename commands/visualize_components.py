from typing import Dict, Any, List
import json
from pathlib import Path
import matplotlib.pyplot as plt
import networkx as nx
from datetime import datetime
import logging

class OSCALVisualizer:
    """Class for creating visualizations of OSCAL data"""
    
    def __init__(self, output_dir: str = "reports"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
    def create_component_graph(self, oscal_file: Dict[str, Any]) -> str:
        """Create a graph visualization of system components and inventory items"""
        G = nx.DiGraph()
        
        try:
            ssp = oscal_file.get("system-security-plan")
            if not ssp:
                raise ValueError("Not a valid SSP file")
                
            system_impl = ssp.get("system-implementation", {})
            
            # Add nodes for components
            components = system_impl.get("components", [])
            for comp in components:
                comp_id = comp.get("uuid", "unknown")
                title = comp.get("title", "Unnamed Component")
                comp_type = comp.get("type", "unknown")
                
                G.add_node(comp_id, 
                          title=title,
                          type=comp_type,
                          node_type="component")
                
                # Add edges for component links
                if "links" in comp:
                    for link in comp["links"]:
                        target_href = link.get("href", "").strip("#")
                        if target_href:
                            G.add_edge(comp_id, target_href, 
                                     relationship=link.get("rel", "unknown"))
                
            # Add nodes for inventory items
            inventory_items = system_impl.get("inventory-items", [])
            for item in inventory_items:
                item_id = item.get("uuid", "unknown")
                desc = item.get("description", "No description")
                
                G.add_node(item_id,
                          title=desc[:30] + "..." if len(desc) > 30 else desc,
                          type="inventory-item",
                          node_type="inventory")
                
                # Add edges for implemented components
                if "implemented-components" in item:
                    for impl_comp in item["implemented-components"]:
                        comp_id = impl_comp.get("component-uuid")
                        if comp_id:
                            G.add_edge(item_id, comp_id,
                                     relationship="implements")
                            
            if len(G.nodes()) == 0:
                logging.warning("No components or inventory items found to visualize")
                return ""
                
            # Generate the visualization
            plt.figure(figsize=(15, 10))
            pos = nx.spring_layout(G, k=2, iterations=50)
            
            # Draw different node types with different colors
            component_nodes = [n for n,d in G.nodes(data=True) 
                             if d.get('node_type') == 'component']
            inventory_nodes = [n for n,d in G.nodes(data=True) 
                             if d.get('node_type') == 'inventory']
            
            # Draw nodes
            nx.draw_networkx_nodes(G, pos, nodelist=component_nodes, 
                                 node_color='lightblue', node_size=2000)
            nx.draw_networkx_nodes(G, pos, nodelist=inventory_nodes,
                                 node_color='lightgreen', node_size=2000)
            
            # Draw edges
            nx.draw_networkx_edges(G, pos)
            
            # Add labels
            labels = {node: f"{data['title']}\n({data['type']})"
                     for node, data in G.nodes(data=True)}
            nx.draw_networkx_labels(G, pos, labels, font_size=8)
            
            # Save the graph
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = self.output_dir / f"component_graph_{timestamp}.png"
            plt.savefig(output_path, bbox_inches='tight', dpi=300)
            plt.close()
            
            return str(output_path)
            
        except Exception as e:
            logging.error(f"Error creating component graph: {str(e)}")
            raise
            
    def generate_html_report(self, oscal_file: Dict[str, Any]) -> str:
        """Generate an HTML report of the OSCAL document"""
        try:
            # Basic template
            html_content = """
            <!DOCTYPE html>
            <html>
            <head>
                <title>OSCAL Component Analysis Report</title>
                <style>
                    body { font-family: Arial, sans-serif; margin: 40px; }
                    .section { margin-bottom: 30px; }
                    .metadata { background-color: #f5f5f5; padding: 15px; border-radius: 5px; }
                    .component { border: 1px solid #ddd; padding: 15px; margin: 10px 0; border-radius: 5px; }
                    .inventory-item { background-color: #f9f9f9; padding: 15px; margin: 10px 0; border-radius: 5px; }
                    .relationship { margin-left: 20px; color: #666; }
                    h2 { color: #333; border-bottom: 2px solid #eee; padding-bottom: 5px; }
                </style>
            </head>
            <body>
            """
            
            ssp = oscal_file.get("system-security-plan")
            if not ssp:
                raise ValueError("Not a valid SSP file")
            
            # Add metadata
            metadata = ssp.get("metadata", {})
            html_content += f"""
            <div class="section metadata">
                <h2>System Information</h2>
                <p><strong>Title:</strong> {metadata.get('title', 'N/A')}</p>
                <p><strong>Version:</strong> {metadata.get('version', 'N/A')}</p>
                <p><strong>Last Modified:</strong> {metadata.get('last-modified', 'N/A')}</p>
            </div>
            """
            
            # Add components section
            system_impl = ssp.get("system-implementation", {})
            components = system_impl.get("components", [])
            
            html_content += """
            <div class="section">
                <h2>System Components</h2>
            """
            
            for comp in components:
                html_content += f"""
                <div class="component">
                    <h3>{comp.get('title', 'Unnamed Component')}</h3>
                    <p><strong>Type:</strong> {comp.get('type', 'N/A')}</p>
                    <p><strong>Description:</strong> {comp.get('description', 'N/A')}</p>
                    
                    {self._format_links(comp.get('links', []))}
                    {self._format_status(comp.get('status', {}))}
                </div>
                """
                
            # Add inventory items section
            inventory_items = system_impl.get("inventory-items", [])
            
            html_content += """
            <div class="section">
                <h2>Inventory Items</h2>
            """
            
            for item in inventory_items:
                html_content += f"""
                <div class="inventory-item">
                    <p><strong>Description:</strong> {item.get('description', 'N/A')}</p>
                    {self._format_properties(item.get('props', []))}
                    {self._format_implemented_components(item.get('implemented-components', []))}
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
            logging.error(f"Error generating HTML report: {str(e)}")
            raise
            
    def _format_links(self, links: List[Dict[str, Any]]) -> str:
        if not links:
            return ""
            
        html = "<p><strong>Links:</strong></p><ul>"
        for link in links:
            html += f"""<li>
                {link.get('text', 'No description')}
                ({link.get('rel', 'unknown')} relationship)
            </li>"""
        html += "</ul>"
        return html
        
    def _format_status(self, status: Dict[str, Any]) -> str:
        if not status:
            return ""
            
        return f"""<p><strong>Status:</strong> {status.get('state', 'N/A')}</p>"""
        
    def _format_properties(self, props: List[Dict[str, Any]]) -> str:
        if not props:
            return ""
            
        html = "<p><strong>Properties:</strong></p><ul>"
        for prop in props:
            html += f"""<li>
                {prop.get('name', 'unnamed')}: {prop.get('value', 'N/A')}
                {f"({prop.get('class')})" if 'class' in prop else ''}
            </li>"""
        html += "</ul>"
        return html
        
    def _format_implemented_components(self, implemented: List[Dict[str, Any]]) -> str:
        if not implemented:
            return ""
            
        html = "<p><strong>Implemented Components:</strong></p><ul>"
        for impl in implemented:
            html += f"""<li>Component ID: {impl.get('component-uuid', 'N/A')}</li>"""
        html += "</ul>"
        return html

def visualize_components(oscal_file: Dict[str, Any]) -> None:
    """Create visual representation of components"""
    visualizer = OSCALVisualizer()
    try:
        # Generate component graph
        graph_path = visualizer.create_component_graph(oscal_file)
        if graph_path:
            print(f"Component graph generated: {graph_path}")
        
        # Generate HTML report
        report_path = visualizer.generate_html_report(oscal_file)
        print(f"HTML report generated: {report_path}")
        
    except Exception as e:
        logging.error(f"Error generating visualizations: {str(e)}")
        print(f"Failed to create visualizations: {str(e)}")
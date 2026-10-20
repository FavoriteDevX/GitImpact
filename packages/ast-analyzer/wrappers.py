import json
import os
import subprocess
from typing import Dict, Any

class HybridASTInteropBridge:
    def __init__(self, node_script_path: str = None):
        """
        Initializes the low-latency subprocess channel to communicate 
        between the Python core and the TypeScript AST parsing layer.
        """
        if node_script_path is None:
            # Resolves path assuming clean monorepo architecture structure
            base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            self.node_script_path = os.path.join(base_dir, "packages", "ast-analyzer", "dist", "cli.js")
        else:
            self.node_script_path = node_script_path

    def call_node_ast_parser(self, original_code: string, modified_code: string) -> Dict[str, Any]:
        """
        Invokes the TypeScript parser binary via secure stdin execution pipeline 
        to circumvent operating system command-line argument size restrictions.
        """
        payload = {
            "original": original_code,
            "modified": modified_code
        }
        
        # Serialize the execution arguments safely into structural JSON
        serialized_payload = json.dumps(payload)

        try:
            # Trigger high-speed decoupled execution thread
            process = subprocess.Popen(
                ["node", self.node_script_path],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )

            # Transmit payloads and capture responses synchronously with automated process termination
            stdout, stderr = process.communicate(input=serialized_payload, timeout=10.0)

            if process.returncode != 0:
                print(f"[!] AST Analyzer subprocess error signal: {stderr}")
                return self._fallback_error_state("SUBPROCESS_EXECUTION_FAILURE")

            # Parse returned structural evaluation context
            return json.loads(stdout)

        except subprocess.TimeoutExpired:
            process.kill()
            print("[!] Critical timeout triggered on TypeScript AST bridge process.")
            return self._fallback_error_state("BRIDGE_TIMEOUT_EXPIRED")
        except Exception as err:
            print(f"[!] Unexpected error state handled on Hybrid Pipeline Bridge: {str(err)}")
            return self._fallback_error_state(f"UNKNOWN_BRIDGE_EXCEPTION: {str(err)}")

    def _fallback_error_state(self, reason: str) -> Dict[str, Any]:
        """
        Graceful resilience system behavior ensuring the core analytics orchestrator 
        never crashes completely if syntax evaluations fail.
        """
        return {
            "structuralChangesDetected": True, # Assume true to avoid dropping potential valid commits
            "cyclomaticComplexityDelta": 0,
            "criticalPatterns": [],
            "errorLog": reason
        }

# Simplified operational export alias matching implementation tasks layout
def call_node_ast_parser(original: str, modified: str) -> Dict[str, Any]:
    bridge = HybridASTInteropBridge()
    return bridge.call_node_ast_parser(original, modified)

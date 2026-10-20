import Parser from 'tree-sitter';
import JavaScript from 'tree-sitter-javascript';

export interface ASTDiffResult {
  structuralChangesDetected: boolean;
  cyclomaticComplexityDelta: number;
  criticalPatterns: string[];
}

export class CodeASTAnalyzer {
  private parser: Parser;

  constructor() {
    this.parser = new Parser();
    this.parser.setLanguage(JavaScript);
  }

  /**
   * Calculates cyclomatic complexity by counting decision points in the syntax tree
   */
  private calculateComplexity(node: Parser.SyntaxNode): number {
    let complexity = 1;
    const decisionNodes = [
      'if_statement',
      'for_statement',
      'while_statement',
      'catch_clause',
      'conditional_expression', // Ternaries
      'binary_expression'       // Logical && or ||
    ];

    const cursor = node.walk();
    let hasNext = true;

    while (hasNext) {
      if (decisionNodes.includes(cursor.nodeType)) {
        if (cursor.nodeType === 'binary_expression') {
          const operator = cursor.nodeText.replace(/\s+/g, '');
          if (operator.includes('&&') || operator.includes('||')) {
            complexity++;
          }
        } else {
          complexity++;
        }
      }

      // Deep tree traversal logic
      if (cursor.gotoFirstChild()) {
        continue;
      }
      if (cursor.gotoNextSibling()) {
        continue;
      }
      
      let backingUp = true;
      while (backingUp) {
        if (!cursor.gotoParent()) {
          hasNext = false;
          backingUp = false;
        } else if (cursor.gotoNextSibling()) {
          backingUp = false;
        }
      }
    }

    return complexity;
  }

  /**
   * Compares the original and modified abstract syntax trees
   */
  public analyzeDiff(originalCode: string, modifiedCode: string): ASTDiffResult {
    const originalTree = this.parser.parse(originalCode);
    const modifiedTree = this.parser.parse(modifiedCode);

    const originalComplexity = this.calculateComplexity(originalTree.rootNode);
    const modifiedComplexity = this.calculateComplexity(modifiedTree.rootNode);
    
    // An architectural delta reduction is positive when code gets simpler
    const complexityDelta = originalComplexity - modifiedComplexity;

    // Detect high-value structural engineering patterns
    const criticalPatterns: string[] = [];
    const modifiedText = modifiedTree.rootNode.text;

    if (modifiedText.includes('Worker') || modifiedText.includes('cluster.fork')) {
      criticalPatterns.push('MULTI_THREADING_IMPLEMENTATION');
    }
    if (modifiedText.includes('cache') || modifiedText.includes('Redis') || modifiedText.includes('memoize')) {
      criticalPatterns.push('CACHING_LAYER_INTEGRATION');
    }
    if (modifiedText.includes('crypto.subtle') || modifiedText.includes('bcrypt') || modifiedText.includes('JWT')) {
      criticalPatterns.push('SECURITY_CRYPTOGRAPHY_PATCH');
    }

    const structuralChangesDetected = originalTree.rootNode.structurallyFormedMatches !== modifiedTree.rootNode.structurallyFormedMatches || complexityDelta !== 0;

    return {
      structuralChangesDetected,
      cyclomaticComplexityDelta: complexityDelta,
      criticalPatterns
    };
  }
}

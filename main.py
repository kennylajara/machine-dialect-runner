"""
FastAPI server for running Machine Dialect code.
Provides an API endpoint that accepts Machine Dialect source code and returns execution results.
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import tempfile
import os
import subprocess
import json
from typing import Optional, Dict, Any
from machine_dialect.compiler import CompilerConfig, Compiler

app = FastAPI(
    title="Machine Dialect Runner",
    description="API for executing Machine Dialect™ code",
    version="1.0.0"
)


class MachineDialectRequest(BaseModel):
    """Request model for Machine Dialect code execution."""
    code: str = Field(..., description="Machine Dialect™ source code to execute")
    debug: bool = Field(False, description="Enable debug mode for execution")


class MachineDialectResponse(BaseModel):
    """Response model for Machine Dialect code execution."""
    success: bool = Field(..., description="Whether execution was successful")
    result: Optional[str] = Field(None, description="Execution result or output")
    error: Optional[str] = Field(None, description="Error message if execution failed")
    debug_info: Optional[Dict[str, Any]] = Field(None, description="Debug information if debug mode enabled")


def compile_and_run_machine_dialect(code: str, debug: bool = False) -> MachineDialectResponse:
    """
    Compile and run Machine Dialect code.
    
    Args:
        code: Machine Dialect source code
        debug: Whether to enable debug mode
        
    Returns:
        MachineDialectResponse with execution results
    """
    temp_source = None
    temp_bytecode = None
    
    try:
        # Create temporary file for source code
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
            f.write(code)
            temp_source = f.name
        
        # Compile the code
        config = CompilerConfig()
        compiler = Compiler(config)
        
        compilation_result = compiler.compile_file(temp_source)
        if not compilation_result:
            return MachineDialectResponse(
                success=False,
                error="Compilation failed"
            )
        
        # The compiler creates a .mdbc file with the same name but different extension
        temp_bytecode = temp_source.replace('.md', '.mdbc')
        
        # Run the compiled bytecode
        cmd = ['machine-dialect', 'run']
        if debug:
            cmd.append('--debug')
        cmd.append(temp_bytecode)
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=30  # 30 second timeout
        )
        
        if result.returncode == 0:
            return MachineDialectResponse(
                success=True,
                result=result.stdout.strip() if result.stdout else "Execution completed successfully",
                debug_info={"stderr": result.stderr} if debug and result.stderr else None
            )
        else:
            return MachineDialectResponse(
                success=False,
                error=result.stderr.strip() if result.stderr else f"Execution failed with exit code {result.returncode}",
                debug_info={"stdout": result.stdout, "stderr": result.stderr} if debug else None
            )
            
    except subprocess.TimeoutExpired:
        return MachineDialectResponse(
            success=False,
            error="Execution timed out after 30 seconds"
        )
    except Exception as e:
        return MachineDialectResponse(
            success=False,
            error=f"Unexpected error: {str(e)}",
            debug_info={"exception_type": type(e).__name__} if debug else None
        )
    finally:
        # Clean up temporary files
        for temp_file in [temp_source, temp_bytecode]:
            if temp_file and os.path.exists(temp_file):
                try:
                    os.unlink(temp_file)
                except OSError:
                    pass


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "Machine Dialect Runner API",
        "description": "Send Machine Dialect™ code to /execute endpoint",
        "docs": "/docs"
    }


@app.post("/execute", response_model=MachineDialectResponse)
async def execute_machine_dialect(request: MachineDialectRequest):
    """
    Execute Machine Dialect™ code.
    
    Args:
        request: Request containing Machine Dialect source code
        
    Returns:
        Execution results
    """
    if not request.code.strip():
        raise HTTPException(status_code=400, detail="Code cannot be empty")
    
    try:
        response = compile_and_run_machine_dialect(request.code, request.debug)
        
        # Return HTTP error for compilation/execution failures
        if not response.success:
            raise HTTPException(status_code=400, detail=response.error)
        
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "machine-dialect-runner"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
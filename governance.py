"""
Governance wrapper para skills de Antigravity.
Uso en cualquier skill Python:

    from governance import guard
    guard(user_input)          # lanza PermissionError si es peligroso
    guard(cmd, agent="skill-name")
"""
import sys
sys.path.insert(0, '/home/juan/.agents/governance')

from engine import GovernanceEngine

_engine = None

def _get_engine():
    global _engine
    if _engine is None:
        _engine = GovernanceEngine()
    return _engine


def guard(text: str, agent: str = "antigravity", raise_on_block: bool = True):
    """
    Evalúa text antes de usarlo (como comando, input, prompt).
    Si raise_on_block=True (default), lanza PermissionError si está bloqueado.
    Siempre retorna el Decision para inspección manual.
    """
    decision = _get_engine().check(text, agent_id=agent)
    if not decision and raise_on_block:
        raise PermissionError(f"Governance bloqueó la acción: {decision.reason}")
    return decision


def check(text: str, agent: str = "antigravity"):
    """Alias de guard con raise_on_block=False — retorna Decision sin lanzar excepción."""
    return _get_engine().check(text, agent_id=agent)

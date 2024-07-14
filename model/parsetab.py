
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'DOT LAMBDA LPAREN NUMBER RPAREN VARexpr : VARexpr : NUMBERexpr : LAMBDA VAR DOT exprexpr : expr exprexpr : LPAREN expr RPAREN'
    
_lr_action_items = {'VAR':([0,1,2,3,4,5,6,8,9,10,11,],[2,2,-1,-2,7,2,2,2,2,-5,2,]),'NUMBER':([0,1,2,3,5,6,8,9,10,11,],[3,3,-1,-2,3,3,3,3,-5,3,]),'LAMBDA':([0,1,2,3,5,6,8,9,10,11,],[4,4,-1,-2,4,4,4,4,-5,4,]),'LPAREN':([0,1,2,3,5,6,8,9,10,11,],[5,5,-1,-2,5,5,5,5,-5,5,]),'$end':([1,2,3,6,10,11,],[0,-1,-2,-4,-5,-3,]),'RPAREN':([2,3,6,8,10,11,],[-1,-2,-4,10,-5,-3,]),'DOT':([7,],[9,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'expr':([0,1,5,6,8,9,11,],[1,6,8,6,6,11,6,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> expr","S'",1,None,None,None),
  ('expr -> VAR','expr',1,'p_expr_var','parser_p.py',44),
  ('expr -> NUMBER','expr',1,'p_expr_num','parser_p.py',48),
  ('expr -> LAMBDA VAR DOT expr','expr',4,'p_expr_lambda','parser_p.py',52),
  ('expr -> expr expr','expr',2,'p_expr_app','parser_p.py',56),
  ('expr -> LPAREN expr RPAREN','expr',3,'p_expr_paren','parser_p.py',60),
]
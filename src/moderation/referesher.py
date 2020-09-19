@attr.s(auto_attribs=True)
class Refresher:
    _machine = automat.MethodicalMachine()
    _wait_and_get: Any
    _backoff: Any
    _exceptions: Sequence[type]
    _max_retries: Optional[int] = attr.ib(default=None)
    _value: Optional = attr.ib(default=None)
    
    @_machine.state()
    def stale():
        pass
    
    @_machine.state()
    def fresh():
        pass
    
    @_machine.input()
    def mark_stale(self):
        pass
        
    @stale.upon(mark_stale, enter=stale)
    @fresh.upon(mark_stale, enter=stale)
    
    @machine.input()
    def get_value(self):
        pass
    
    @machine.output()
    def get_fresh_value(self):
        return self._value
    
    @machine.output()
    def refresh(self):
        retries = range(self._max_retries - 1) if self._max_retries is not None else itertools.count()
        for retry in retries:
            self._wait_and_get(next(self._backoff()))
        
    @fresh.upon(get_value, enter=fresh, outputs=[self.get_fresh_value])
    @stale.upon(get_value, enter=fresh, outputs=[self.refresh])

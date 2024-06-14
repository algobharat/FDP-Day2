from algopy import ARC4Contract, arc4, UInt64


class HelloWorld(ARC4Contract):
    @arc4.abimethod()
    def hello(self, name: arc4.String) -> arc4.String:
        return "Hello, " + name

    @arc4.abimethod()
    def addition (self, firnum: UInt64,secnum : UInt64) -> UInt64:
        total = firnum + secnum
        return total
    
    @arc4.abimethod()
    def temperature(self, temperature: UInt64) -> None:
        self.global_uint64_simplified = temperature
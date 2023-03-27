export default class Holder {
    constructor (address, amount, owner, inCirc, supply) {
        this.address = address;
        this.owner = owner;
        this.amount = amount;
        this.stake = amount/supply;
        this.inCirc = inCirc;
    }
    changeStatus(bool) {
        this.inCirc = bool;
    }
}
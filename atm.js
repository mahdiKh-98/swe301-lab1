document.addEventListener("DOMContentLoaded", () => {
    const screen = document.querySelector('.screen');
    const atmContainer = document.querySelector('.atm-container');
    const keypad = document.querySelector('.keypad');
    const cardSlot = document.querySelector('.card-slot');

    let pinEntry = '';
    let isCardInserted = false;
    let accountBalance = 500; // Example balance

    atmContainer.addEventListener('click', () => {
        if (!isCardInserted) {
            insertCard();
        }
    });

    keypad.addEventListener('click', (event) => {
        const value = event.target.textContent;

        if (!isCardInserted || !value) return;

        switch (value) {
            case 'Cancel':
                resetATM();
                break;
            case 'Clear':
                pinEntry = '';
                updateScreen('Enter your PIN');
                break;
            case 'Enter':
                if (pinEntry.length === 4) {
                    verifyPIN();
                }
                break;
            case '<':
                if (pinEntry.length > 0) {
                    pinEntry = pinEntry.slice(0, -1);
                    updateScreen('*'.repeat(pinEntry.length));
                }
                break;
            default:
                if (pinEntry.length < 4 && !isNaN(value)) {
                    pinEntry += value;
                    updateScreen('*'.repeat(pinEntry.length));
                }
        }
    });

    function insertCard() {
        isCardInserted = true;
        cardSlot.classList.add('inserting');
        setTimeout(() => {
            updateScreen('Enter your PIN');
        }, 1000);
    }

    function verifyPIN() {
        if (pinEntry === '3333') {
            updateScreen('PIN Accepted');
            setTimeout(() => {
                displayTransactions();
            }, 1500);
        } else {
            updateScreen('Invalid PIN');
            setTimeout(() => {
                pinEntry = '';
                updateScreen('Enter your PIN');
            }, 1500);
        }
    }

    function resetATM() {
        isCardInserted = false;
        pinEntry = '';
        cardSlot.classList.remove('inserting');
        updateScreen('Please insert your card');
    }

    function displayTransactions() {
        screen.innerHTML = `
            <button class="transaction-button" onclick="startWithdrawal()">Withdraw</button>
            <button class="transaction-button">Deposit</button>
            <button class="transaction-button">Balance Check</button>
            <button class="transaction-button">Paying Bills</button>
        `;
    }

    window.startWithdrawal = function() {
        screen.innerHTML = `
            <div>Account Balance: $${accountBalance}</div>
            <div class="withdraw-options">
                <button onclick="withdrawAmount(20)">$20</button>
                <button onclick="withdrawAmount(50)">$50</button>
                <button onclick="withdrawAmount(100)">$100</button>
                <button onclick="withdrawAmount(200)">$200</button>
            </div>
            <div>
                <input type="number" id="customAmount" placeholder="Enter amount manually">
                <button onclick="customWithdraw()">Submit</button>
            </div>
        `;
    };

    window.withdrawAmount = function(amount) {
        processWithdrawal(amount);
    };

    window.customWithdraw = function() {
        const customAmount = parseFloat(document.getElementById('customAmount').value);
        if (customAmount > 0) {
            processWithdrawal(customAmount);
        } else {
            alert("Please enter a valid amount!");
        }
    };
    function dispenseMoney(amount) {
        screen.innerHTML = `
            <div class="dispensing">
                <p>Dispensing money: $${amount}</p>
                <p>Thank you for your transaction.</p>
            </div>
        `;
        setTimeout(() => {
            location.reload(); // Reload the page after 5 seconds
        }, 2000);
    }
     function updateScreen(message) {
        screen.textContent = message;
    }
    function processWithdrawal(amount) {
        if (amount > accountBalance) {
            // Insufficient funds error
            screen.innerHTML = `
                <div class="error-message">
                    The requested amount exceeds the available balance.
                </div>
                <button class="back-button" onclick="startWithdrawal()">Back to Withdrawal</button>
            `;
        } else if (amount <= 0) {
            // Invalid amount error
            screen.innerHTML = `
                <div class="error-message">
                    Please enter a valid withdrawal amount.
                </div>
                <button class="back-button" onclick="startWithdrawal()">Back to Withdrawal</button>
            `;
        } else {
            // Valid amount: Deduct from balance and prompt for receipt
            accountBalance -= amount;
    
            // Attach proper event handlers for Yes and No buttons
            screen.innerHTML = `
                <div class="receipt-prompt">
                    <p>Do you want to print a receipt?</p>
                    <button class="yes-button" onclick="printReceipt(${amount})">Yes</button>
                    <button id="no-button" class="no-button">No</button>
                </div>
            `;
    
            // Add event listener to "No" button
            const noButton = document.getElementById("no-button");
            noButton.addEventListener("click", () => dispenseMoney(amount));
        }
    }
    

    window.printReceipt = function(amount) {
        const now = new Date();
        const receipt = `
            Bank: Home Bank
            Branch: Cyprus Branch
            Date: ${now.toLocaleDateString()}
            Time: ${now.toLocaleTimeString()}
            Amount: $${amount}
            Currency: USD
        `;
        alert(receipt); // Simulate receipt printing
        screen.innerHTML = `
        <div class="thank-you">
            <p>Thank you for banking with us.</p>
        </div>
    `;
    setTimeout(() => {
        location.reload(); // Reload the page after 5 seconds
    }, 2000);
    };

   
    
});

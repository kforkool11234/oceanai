# Product Specifications - E-Shop Checkout

## Features

### Cart & Pricing
- **Items**: Users can adjust quantity of items.
- **Total Calculation**: Total price = (Item Prices * Quantities) - Discount + Shipping.

### Discount Codes
- **SAVE15**: Applies a 15% discount to the item subtotal (before shipping).
- **Invalid Codes**: Should show an error message "Invalid Code".

### Shipping Methods
- **Standard**: Free shipping. Delivery in 5-7 days.
- **Express**: Flat rate of $10. Delivery in 2-3 days.

### Payment Methods
- **Credit Card**: Default option.
- **PayPal**: Alternative option.

### Form Validation
- **Full Name**: Required.
- **Email**: Required, must contain '@'.
- **Address**: Required.
- **Error Messages**: Must be displayed inline in red text below the invalid field.

### Success State
- Upon valid submission, hide the "Pay Now" button and show "Payment Successful!" in green.

// static/main.js

console.log("Sanity check!");

// Get Stripe publishable key
fetch("/subscriptions/config/")
.then((result) => { return result.json(); })
.then((data) => {
  console.log("Sanity check!");
  // Initialize Stripe.js
  const stripe = Stripe(data.publicKey);

  // new
  // Event handler
  let submitBtn = document.querySelector("#submitBtn");
  if (submitBtn !== null) {
    submitBtn.addEventListener("click", () => {
    // Get Checkout Session ID'
    console.log("i am in the blog")
    fetch("/subscriptions/create-checkout-session/")
      .then((result) => { return result.json(); })
      .then((data) => {
        console.log(data);
        // Redirect to Stripe Checkout
        return stripe.redirectToCheckout({sessionId: data.sessionId})
      })
      .then((res) => {
        console.log(res);
      });
    });
  }
});
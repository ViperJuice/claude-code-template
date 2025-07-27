package main

import (
    "bytes"
    "encoding/json"
    "fmt"
    "net/http"
    "time"

    "github.com/gin-gonic/gin"
    "github.com/google/uuid"
    "github.com/shopspring/decimal"
)

type Order struct {
    OrderID     uuid.UUID       `json:"order_id"`
    CustomerID  string          `json:"customer_id"`
    Items       []OrderItem     `json:"items"`
    TotalAmount decimal.Decimal `json:"total_amount"`
    Status      string          `json:"status"`
    CreatedAt   time.Time       `json:"created_at"`
}

type OrderItem struct {
    ProductID string          `json:"product_id"`
    Quantity  int             `json:"quantity"`
    Price     decimal.Decimal `json:"price"`
}

type PaymentRequest struct {
    OrderID       uuid.UUID       `json:"order_id"`
    Amount        decimal.Decimal `json:"amount"`
    Currency      string          `json:"currency"`
    PaymentMethod string          `json:"payment_method"`
}

type PaymentResponse struct {
    PaymentID   uuid.UUID `json:"payment_id"`
    OrderID     uuid.UUID `json:"order_id"`
    Status      string    `json:"status"`
    ProcessedAt time.Time `json:"processed_at"`
}

var orders = make(map[uuid.UUID]*Order)

func createOrder(c *gin.Context) {
    var order Order
    if err := c.ShouldBindJSON(&order); err != nil {
        c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
        return
    }

    order.OrderID = uuid.New()
    order.Status = "pending"
    order.CreatedAt = time.Now()

    // Calculate total
    total := decimal.Zero
    for _, item := range order.Items {
        total = total.Add(item.Price.Mul(decimal.NewFromInt(int64(item.Quantity))))
    }
    order.TotalAmount = total

    // Process payment
    paymentReq := PaymentRequest{
        OrderID:       order.OrderID,
        Amount:        order.TotalAmount,
        Currency:      "USD",
        PaymentMethod: "credit_card",
    }

    paymentResp, err := processPayment(paymentReq)
    if err != nil {
        order.Status = "payment_failed"
        c.JSON(http.StatusBadRequest, gin.H{"error": "Payment failed"})
        return
    }

    if paymentResp.Status == "approved" {
        order.Status = "confirmed"
    } else {
        order.Status = "payment_failed"
    }

    orders[order.OrderID] = &order
    c.JSON(http.StatusCreated, order)
}

func processPayment(req PaymentRequest) (*PaymentResponse, error) {
    client := &http.Client{Timeout: 5 * time.Second}
    
    jsonData, err := json.Marshal(req)
    if err != nil {
        return nil, err
    }

    resp, err := client.Post("http://localhost:8001/process", "application/json", bytes.NewBuffer(jsonData))
    if err != nil {
        return nil, err
    }
    defer resp.Body.Close()

    var paymentResp PaymentResponse
    if err := json.NewDecoder(resp.Body).Decode(&paymentResp); err != nil {
        return nil, err
    }

    return &paymentResp, nil
}

func getOrder(c *gin.Context) {
    orderID, err := uuid.Parse(c.Param("id"))
    if err != nil {
        c.JSON(http.StatusBadRequest, gin.H{"error": "Invalid order ID"})
        return
    }

    order, exists := orders[orderID]
    if !exists {
        c.JSON(http.StatusNotFound, gin.H{"error": "Order not found"})
        return
    }

    c.JSON(http.StatusOK, order)
}

func health(c *gin.Context) {
    c.JSON(http.StatusOK, gin.H{
        "status":  "healthy",
        "service": "order-service",
    })
}

func main() {
    r := gin.Default()

    r.GET("/health", health)
    r.POST("/orders", createOrder)
    r.GET("/orders/:id", getOrder)

    fmt.Println("Starting Order Service on http://localhost:8002")
    r.Run(":8002")
}
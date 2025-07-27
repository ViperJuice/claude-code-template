use actix_web::{web, App, HttpResponse, HttpServer, Result};
use serde::{Deserialize, Serialize};
use uuid::Uuid;
use rust_decimal::Decimal;
use chrono::{DateTime, Utc};

#[derive(Debug, Serialize, Deserialize)]
struct PaymentRequest {
    order_id: Uuid,
    amount: Decimal,
    currency: String,
    payment_method: String,
}

#[derive(Debug, Serialize, Deserialize)]
struct PaymentResponse {
    payment_id: Uuid,
    order_id: Uuid,
    status: String,
    processed_at: DateTime<Utc>,
}

async fn process_payment(payment: web::Json<PaymentRequest>) -> Result<HttpResponse> {
    // Simulate payment processing
    let response = PaymentResponse {
        payment_id: Uuid::new_v4(),
        order_id: payment.order_id,
        status: "approved".to_string(),
        processed_at: Utc::now(),
    };
    
    Ok(HttpResponse::Ok().json(response))
}

async fn health() -> Result<HttpResponse> {
    Ok(HttpResponse::Ok().json(serde_json::json!({
        "status": "healthy",
        "service": "payment-service"
    })))
}

#[actix_web::main]
async fn main() -> std::io::Result<()> {
    tracing_subscriber::fmt::init();
    
    println!("Starting Payment Service on http://localhost:8001");
    
    HttpServer::new(|| {
        App::new()
            .route("/health", web::get().to(health))
            .route("/process", web::post().to(process_payment))
    })
    .bind("127.0.0.1:8001")?
    .run()
    .await
}
use actix_web::{get, http::header::ContentType, web, App, HttpResponse, HttpServer, Responder};
use serde::Deserialize;
use sherpa_rs::tts::{KokoroTts, KokoroTtsConfig};
use sherpa_rs::write_audio_file;

#[derive(Deserialize)]
struct GenerateParams {
    text: String,
    speaker_id: i32,
}

#[get("/")]
async fn hello() -> impl Responder {
    HttpResponse::Ok()
        .content_type(ContentType::html())
        .body("Hello world!")
}

#[get("/generate")]
async fn generate(params: web::Query<GenerateParams>) -> impl Responder {
    let config: KokoroTtsConfig = KokoroTtsConfig {
        model: "./kokoro-en-v0_19/model.onnx".to_string(),
        voices: "./kokoro-en-v0_19/voices.bin".into(),
        tokens: "./kokoro-en-v0_19/tokens.txt".into(),
        data_dir: "./kokoro-en-v0_19/espeak-ng-data".into(),
        length_scale: 1.0,
        ..Default::default()
    };
    let mut tts = KokoroTts::new(config);

    // 0->af, 1->af_bella, 2->af_nicole, 3->af_sarah, 4->af_sky, 5->am_adam
    // 6->am_michael, 7->bf_emma, 8->bf_isabella, 9->bm_george, 10->bm_lewis

    let audio = tts.create(&params.text, params.speaker_id, 1.0).unwrap();

    write_audio_file("audio.wav", &audio.samples, audio.sample_rate);

    HttpResponse::Ok()
        .content_type(ContentType::json())
        .body("Created audio.wav")
}

#[actix_web::main]
async fn main() -> std::io::Result<()> {
    HttpServer::new(|| App::new().service(hello).service(generate))
        .bind(("0.0.0.0", 8001))?
        .run()
        .await
}

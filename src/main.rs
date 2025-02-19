use actix_files::NamedFile;
use actix_web::{
    get, http::header::ContentType, middleware::Logger, web, App, HttpResponse, HttpServer,
    Responder,
};
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
async fn generate(
    params: web::Query<GenerateParams>,
) -> actix_web::Result<NamedFile, actix_web::Error> {
    if params.text.trim().is_empty() {
        return Err(actix_web::error::ErrorBadRequest("Text cannot be empty"));
    };

    if !(0..=10).contains(&params.speaker_id) {
        return Err(actix_web::error::ErrorBadRequest(
            "Speaker ID must be between 0 and 10",
        ));
    };

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
    let _ = write_audio_file("assets/audio.wav", &audio.samples, audio.sample_rate);
    Ok(NamedFile::open("assets/audio.wav")?)
}

#[actix_web::main]
async fn main() -> std::io::Result<()> {
    env_logger::init_from_env(env_logger::Env::new().default_filter_or("info"));
    log::info!("starting HTTP server at http://localhost:8001");
    HttpServer::new(|| {
        App::new()
            .service(hello)
            .service(generate)
            .wrap(Logger::default())
    })
    .bind(("0.0.0.0", 8001))?
    .run()
    .await
}

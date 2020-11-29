#![feature(proc_macro_hygiene, decl_macro)]

#[macro_use] 
extern crate diesel;
#[macro_use] 
extern crate rocket_contrib;
#[macro_use] 
extern crate rocket;

mod schema;

use rocket::response::{content};
use diesel::prelude::*;
use schema::links;

// the database settings is in diesel.toml
#[database("sqlite_logs")]
struct LogsDbConn(diesel::SqliteConnection);


#[derive(Queryable)]
struct Link {
    shortlink: String,
    url: String
}


#[get("/")]
fn index() -> content::Json<&'static str> {
    content::Json("{\"message\":\"pastelink rust backend\"}")
}

#[get("/about")]
fn about() -> String {
    return format!("link for");
}

#[get("/l/<_shortlink>")]
fn redirect(conn: LogsDbConn, _shortlink: String) -> String {
    // return Redirect()
    let data = links::table
        .filter(links::shortlink.eq(&_shortlink))
        .get_result::<Link>(&*conn);
    match data {
        Ok(link) => {
            return format!("hello {}->{}", link.shortlink, link.url);
        },
        Err(e) =>{
            return format!("redirect for {}", e);
        }
    }
}

#[get("/shortlinks")]
fn shortlinks() -> String {
    return format!("link for");
}

// #[post("/shortlinks", format="application/json", data="<link>")]
// fn linkpost(link: Link) -> String {
//     return format!("post thiz lelz");
// }

// #[get("/shortlinks/<id>/delete")]
// fn delete_shortlink(id: String, user: User) -> String {
//     return format!("deleted {}", id);
// }

#[get("/shortlinks/<id>/delete", rank=3)]
fn delete_shortlink_redirect(id: String) -> String {
    return format!("you cannot delete {}", id);
}

fn main() {
    rocket::ignite()
        .mount("/", routes![
            index, 
            redirect, 
            shortlinks,
            about,
            delete_shortlink_redirect])
        .attach(LogsDbConn::fairing())
    .launch();
}